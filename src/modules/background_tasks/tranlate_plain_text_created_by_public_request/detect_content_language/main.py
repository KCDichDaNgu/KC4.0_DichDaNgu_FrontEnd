from datetime import datetime
import logging
from infrastructure.configs.language import LanguageEnum
from infrastructure.configs.translation_history import TranslationHistoryStatus
from core.utils.common import chunk_arr


from typing import List
from uuid import UUID

from infrastructure.configs.main import GlobalConfig, get_cnf, get_mongodb_instance
from infrastructure.configs.translation_request import (
    LanguageNotYetDetectedResultFileSchemaV1, NotYetTranslatedResultFileSchemaV1, TaskTypeEnum, TranslationStepEnum, StepStatusEnum
)

from infrastructure.adapters.language_detector.main import LanguageDetector

from modules.translation_request.database.translation_request.repository import TranslationRequestRepository, TranslationRequestEntity
from modules.translation_request.database.translation_request_result.repository import TranslationRequestResultRepository, TranslationRequestResultEntity
from modules.translation_request.database.translation_history.repository import TranslationHistoryRepository, TranslationHistoryEntity

import asyncio
import aiohttp

from infrastructure.adapters.logger import Logger

config: GlobalConfig = get_cnf()
db_instance = get_mongodb_instance()

PUBLIC_LANGUAGE_DETECTION_API_CONF = config.PUBLIC_LANGUAGE_DETECTION_API
ALLOWED_CONCURRENT_REQUEST = PUBLIC_LANGUAGE_DETECTION_API_CONF.ALLOWED_CONCURRENT_REQUEST

translationRequestRepository = TranslationRequestRepository()
translationRequestResultRepository = TranslationRequestResultRepository()
transationHistoryRepository = TranslationHistoryRepository()

languageDetector = LanguageDetector()

logger = Logger('Task: translate_plain_text_in_public_request.detect_content_language')

async def read_task_result(
    tasks_result: List[TranslationRequestResultEntity], 
    tasks: List[TranslationRequestEntity],
    translations_history: List[TranslationHistoryEntity]
):
    
    valid_tasks_mapper = {}

    task_id_1 = list(map(lambda t: t.id.value, tasks))
    task_id_2 = list(map(lambda ts: ts.props.task_id.value, tasks_result))
    task_id_3 = list(map(lambda th: th.props.task_id.value, translations_history))

    intersection_tasks_id = list(set(task_id_1) & set(task_id_2) & set(task_id_3))
    
    for task_id in intersection_tasks_id:

        task = list(filter(lambda ts: ts.id.value == task_id, tasks))[0]
        task_result = list(filter(lambda ts: ts.props.task_id.value == task_id, tasks_result))[0]
        trans_history = list(filter(lambda ts: ts.props.task_id.value == task_id, translations_history))[0]

        try: 
            data = await task_result.read_data_from_file()
            
            if data['status'] == LanguageNotYetDetectedResultFileSchemaV1(
                source_text='', 
                target_lang=LanguageEnum.vi.value
            ).status:

                valid_tasks_mapper[task_id] = {
                    'task_result_content': data,
                    'task_result': task_result,
                    'trans_history': trans_history,
                    'task': task
                }

        except Exception as e:
            logger.error(e)

            print(e)

    valid_tasks_id = valid_tasks_mapper.keys()

    invalid_tasks = list(filter(lambda t: t.id.value not in valid_tasks_id, tasks))

    return valid_tasks_mapper, invalid_tasks

async def mark_invalid_tasks(invalid_tasks: List[TranslationRequestEntity]):

    result = []
    
    with db_instance.session() as session:
        with session.start_transaction():

            update_request = []

            for task in invalid_tasks:

                update_request.append(
                    translationRequestRepository.update(
                        task, 
                        dict(step_status=StepStatusEnum.cancelled.value),
                        conditions={}
                    )
                )

            result = await asyncio.gather(*update_request)

    return result

async def main():

    logger.log(
        level=logging.INFO,
        msg=f'New task translate_plain_text_in_public_request.detect_content_language run in {datetime.now()}'
    )

    print(f'New task translate_plain_text_in_public_request.detect_content_language run in {datetime.now()}')
    
    tasks = await translationRequestRepository.find_many(
        params=dict(
            task_type=TaskTypeEnum.public_plain_text_translation.value,
            current_step=TranslationStepEnum.detecting_language.value,
            step_status=StepStatusEnum.not_yet_processed.value,
            expired_date={
                "$gt": datetime.now()
            }
        ),
        limit=ALLOWED_CONCURRENT_REQUEST * 10
    )

    tasks_id = list(map(lambda task: task.id.value, tasks))

    tasks_result_and_trans_history_req = [
        translationRequestResultRepository.find_many(
            params=dict(
                task_id={
                    '$in': list(map(lambda t: UUID(t), tasks_id))
                },
                step=TranslationStepEnum.detecting_language.value
            )
        ),
        transationHistoryRepository.find_many(
            params=dict(
                task_id={
                    '$in': list(map(lambda t: UUID(t), tasks_id))
                }
            )
        )
    ]
    
    tasks_result, translations_history = await asyncio.gather(*tasks_result_and_trans_history_req)
    
    valid_tasks_mapper, invalid_tasks = await read_task_result(
        tasks=tasks, 
        tasks_result=tasks_result,
        translations_history=translations_history
    )
    
    await mark_invalid_tasks(invalid_tasks)

    try:

        valid_tasks_id = list(map(lambda t: t.id.value, tasks))

        chunked_tasks_id = chunk_arr(valid_tasks_id, ALLOWED_CONCURRENT_REQUEST)

        for chunk in chunked_tasks_id:
            
            await execute_in_batch(valid_tasks_mapper, chunk)

    except Exception as e:
        logger.error(e)

        print(e)

    logger.log(
        level=logging.INFO,
        msg=f'An task translate_plain_text_in_public_request.detect_content_language end in {datetime.now()}'
    )

    print(f'An task translate_plain_text_in_public_request.detect_content_language end in {datetime.now()}')
            

async def execute_in_batch(valid_tasks_mapper, tasks_id):

    loop = asyncio.get_event_loop()

    connector = aiohttp.TCPConnector(limit=ALLOWED_CONCURRENT_REQUEST)

    async with aiohttp.ClientSession(connector=connector, loop=loop) as session:

        api_requests = []

        for task_id in tasks_id:
            
            source_text = valid_tasks_mapper[task_id]['task_result_content']['source_text']

            api_requests.append(
                languageDetector.detect(
                    text=source_text, 
                    session=session
                )
            )

        api_results = await asyncio.gather(*api_requests)
        
        with db_instance.session() as session:

            with session.start_transaction():
    
                update_request = []

                for task_id, api_result in zip(tasks_id, api_results):

                    task_result = valid_tasks_mapper[task_id]['task_result'],
                    trans_history = valid_tasks_mapper[task_id]['trans_history'],
                    task = valid_tasks_mapper[task_id]['task']
                    task_result_content = valid_tasks_mapper[task_id]['task_result_content']
                    
                    new_saved_content = NotYetTranslatedResultFileSchemaV1(
                        source_text=task_result_content['source_text'],
                        source_lang=api_result.lang,
                        target_lang=task_result_content['target_lang']
                    )

                    if isinstance(task_result, tuple):
                        task_result = task_result[0]

                    if isinstance(trans_history, tuple):
                        trans_history = trans_history[0]
                
                    await translationRequestRepository.update(
                        task, 
                        dict(
                            step_status=StepStatusEnum.not_yet_processed.value,
                            current_step=TranslationStepEnum.translating_language.value
                        )
                    )
                
                    await translationRequestResultRepository.update(
                        task_result, 
                        dict(
                            step=TranslationStepEnum.translating_language.value
                        )
                    )
                    
                    await transationHistoryRepository.update(
                        trans_history, 
                        dict(
                            status=TranslationHistoryStatus.translating.value
                        )
                    )

                    await task_result.save_request_result_to_file(
                        content=new_saved_content.json()
                    )
