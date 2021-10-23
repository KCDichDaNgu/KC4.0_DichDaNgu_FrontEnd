from datetime import datetime
import logging
from core.utils.file import get_full_path
from infrastructure.adapters.content_translator.main import ContentTranslator
from infrastructure.adapters.speech_recognitor.main import SpeechRecognitor
from infrastructure.configs.language import LanguageEnum
from infrastructure.configs.speech_recognition_history import SpeechRecognitionHistoryStatus
from core.utils.common import chunk_arr


from typing import List
from uuid import UUID

from infrastructure.configs.main import GlobalConfig, get_cnf, get_mongodb_instance
from infrastructure.configs.speech_recognition_task import SPEECH_RECOGNITION_RESULT_FILE_STATUS, SpeechRecognitionTask_ConvertedResultFileSchemaV1, SpeechRecognitionTask_ConvertingResultFileSchemaV1, SpeechRecognitionTask_TranslatedResultFileSchemaV1, get_speech_recognition_file_path, get_speech_recognition_converted_file_name, get_speech_recognition_translated_file_name
from infrastructure.configs.task import (
    SpeechRecognitionTaskStepEnum, 
    StepStatusEnum
)


from infrastructure.configs.task import (
    SpeechRecognitionTaskStepEnum,
    SpeechRecognitionTaskNameEnum,
)

import asyncio
import aiohttp

from infrastructure.adapters.logger import Logger
from modules.speech_recognition_request.database.speech_recognition_history.repository import SpeechRecognitionHistoryRepository
from modules.speech_recognition_request.database.speech_recognition_request.repository import SpeechRecognitionRequestRepository
from modules.speech_recognition_request.database.speech_recognition_request_result.repository import SpeechRecognitionRequestResultRepository
from modules.speech_recognition_request.domain.entities.speech_recognition_request import SpeechRecognitionRequestEntity
from modules.speech_recognition_request.domain.entities.speech_recognition_request_result import SpeechRecognitionRequestResultEntity
from modules.translation_request.domain.entities.translation_history import TranslationHistoryEntity

config: GlobalConfig = get_cnf()
db_instance = get_mongodb_instance()

PUBLIC_LANGUAGE_DETECTION_API_CONF = config.PUBLIC_LANGUAGE_DETECTION_API
ALLOWED_CONCURRENT_REQUEST = PUBLIC_LANGUAGE_DETECTION_API_CONF.ALLOWED_CONCURRENT_REQUEST

speech_recognition_request_repository = SpeechRecognitionRequestRepository()
speech_recognition_request_result_repository = SpeechRecognitionRequestResultRepository()
speech_recognition_history_repository = SpeechRecognitionHistoryRepository()

contentTranslator = ContentTranslator()

logger = Logger('Task: translate_speech_in_public_request')

async def read_task_result(
    tasks_result: List[SpeechRecognitionRequestResultEntity], 
    tasks: List[SpeechRecognitionRequestEntity],
    speech_recognitions_history: List[TranslationHistoryEntity]
):
    
    valid_tasks_mapper = {}

    task_id_1 = list(map(lambda t: t.id.value, tasks))
    task_id_2 = list(map(lambda ts: ts.props.task_id.value, tasks_result))
    task_id_3 = list(map(lambda th: th.props.task_id.value, speech_recognitions_history))

    intersection_tasks_id = list(set(task_id_1) & set(task_id_2) & set(task_id_3))

    for task_id in intersection_tasks_id:

        task = list(filter(lambda ts: ts.id.value == task_id, tasks))[0]
        task_result = list(filter(lambda ts: ts.props.task_id.value == task_id, tasks_result))[0]
        recognize_history = list(filter(lambda ts: ts.props.task_id.value == task_id, speech_recognitions_history))[0]

        try: 
            data = await task_result.read_data_from_file()
            
            if data['status'] == SpeechRecognitionTask_ConvertedResultFileSchemaV1(
                source_file_full_path='',
                converted_file_full_path='',
                source_lang=LanguageEnum.en.value,
                target_lang=LanguageEnum.vi.value,
                job_id='',
                task_name=SpeechRecognitionTaskNameEnum.public_speech_translation.value
            ).status:
                valid_tasks_mapper[task_id] = {
                    'task_result_content': data,
                    'task_result': task_result,
                    'recognize_history': recognize_history,
                    'task': task
                }

        except Exception as e:
            logger.error(e)

            print(e)

    valid_tasks_id = valid_tasks_mapper.keys()

    invalid_tasks = list(filter(lambda t: t.id.value not in valid_tasks_id, tasks))

    invalid_tasks_id = list(map(lambda t: t.id.value, invalid_tasks))

    invalid_tasks_mapper = {}

    for task_id in invalid_tasks_id:

        task = list(filter(lambda ts: ts.id.value == task_id, tasks))[0]
        task_result = list(filter(lambda ts: ts.props.task_id.value == task_id, tasks_result))[0]
        recognize_history = list(filter(lambda ts: ts.props.task_id.value == task_id, speech_recognitions_history))[0]
        invalid_tasks_mapper[task_id] = {
            'task_result': task_result,
            'recognize_history': recognize_history,
            'task': task
        }

    return valid_tasks_mapper, invalid_tasks_mapper

async def mark_invalid_tasks(invalid_tasks_mapper):

    result = []
    
    async with db_instance.session() as session:
        async with session.start_transaction():

            update_request = []
            
            for task_id in invalid_tasks_mapper.keys():

                task_result = invalid_tasks_mapper[task_id]['task_result'],
                recognize_history = invalid_tasks_mapper[task_id]['recognize_history'],
                task = invalid_tasks_mapper[task_id]['task']

                if isinstance(task_result, tuple):
                    task_result = task_result[0]

                if isinstance(recognize_history, tuple):
                    recognize_history = recognize_history[0]
                    
                update_request.append(
                    speech_recognition_request_repository.update(
                        task, 
                        dict(step_status=StepStatusEnum.cancelled.value),
                        conditions={}
                    )
                )
                
                update_request.append(
                    speech_recognition_history_repository.update(
                        recognize_history, 
                        dict(
                            status=SpeechRecognitionHistoryStatus.cancelled.value
                        )
                    )
                )

            result = await asyncio.gather(*update_request)

    return result

async def main():

    logger.debug(
        msg=f'New task translate_speech_in_public_request run in {datetime.now()}'
    )

    print(f'New task translate_speech_in_public_request run in {datetime.now()}')
    
    try:
        tasks = await speech_recognition_request_repository.find_many(
            params=dict(
                task_name=SpeechRecognitionTaskNameEnum.public_speech_translation.value,
                current_step=SpeechRecognitionTaskStepEnum.translating_speech.value,
                step_status=StepStatusEnum.in_progress.value,
                expired_date={
                    "$gt": datetime.now()
                }
            ),
            limit=ALLOWED_CONCURRENT_REQUEST * 10
        )

        tasks_id = list(map(lambda task: task.id.value, tasks))

        if len(tasks_id) == 0: 
            logger.debug(
                msg=f'An task translate_speech_in_public_request end in {datetime.now()}\n'
            )
            print(f'An task translate_speech_in_public_request end in {datetime.now()}\n')
            return

        tasks_result_and_recognition_history_req = [
            speech_recognition_request_result_repository.find_many(
                params=dict(
                    task_id={
                        '$in': list(map(lambda t: UUID(t), tasks_id))
                    },
                    step=SpeechRecognitionTaskStepEnum.translating_speech.value
                )
            ),
            speech_recognition_history_repository.find_many(
                params=dict(
                    task_id={
                        '$in': list(map(lambda t: UUID(t), tasks_id))
                    }
                )
            )
        ]

        tasks_result, speech_recognitions_history = await asyncio.gather(*tasks_result_and_recognition_history_req)

        valid_tasks_mapper, invalid_tasks_mapper = await read_task_result(
            tasks=tasks, 
            tasks_result=tasks_result,
            speech_recognitions_history=speech_recognitions_history
        )
        
        await mark_invalid_tasks(invalid_tasks_mapper)

        valid_tasks_id = list(map(lambda t: t.id.value, tasks))

        chunked_tasks_id = list(chunk_arr(valid_tasks_id, ALLOWED_CONCURRENT_REQUEST))
        
        for chunk in chunked_tasks_id:
            
            await execute_in_batch(valid_tasks_mapper, chunk)

    except Exception as e:
        logger.error(e)
        
        print(e)

    logger.debug(
        msg=f'An task translate_speech_in_public_request end in {datetime.now()}\n'
    )

    print(f'An task translate_speech_in_public_request end in {datetime.now()}\n')
            

async def execute_in_batch(valid_tasks_mapper, tasks_id):

    loop = asyncio.get_event_loop()

    connector = aiohttp.TCPConnector(limit=ALLOWED_CONCURRENT_REQUEST)

    async with aiohttp.ClientSession(connector=connector, loop=loop) as session:

        api_requests = []

        for task_id in tasks_id:
            converted_file_full_path = valid_tasks_mapper[task_id]['task_result_content']['converted_file_full_path']
            source_file_full_path = valid_tasks_mapper[task_id]['task_result_content']['source_file_full_path']
            source_lang = valid_tasks_mapper[task_id]['task_result_content']['source_lang']
            target_lang = valid_tasks_mapper[task_id]['task_result_content']['target_lang']

            converted_file = open(converted_file_full_path, "r")

            converted_text = (converted_file.read())

            if source_lang == target_lang:
                async with db_instance.session() as session:
                    async with session.start_transaction():

                        translated_file_name = f'{get_speech_recognition_translated_file_name()}.txt'
                        translated_file_path = get_speech_recognition_file_path(task_id, translated_file_name)
                        translated_file_full_path = get_full_path(translated_file_path)

                        converted_file.save(translated_file_full_path)
                        
                        update_request = []
                        task_result = valid_tasks_mapper[task_id]['task_result'],
                        trans_history = valid_tasks_mapper[task_id]['trans_history'],
                        task = valid_tasks_mapper[task_id]['task']
                        task_result_content = valid_tasks_mapper[task_id]['task_result_content']
                        
                        new_saved_content = SpeechRecognitionTask_TranslatedResultFileSchemaV1(
                            source_file_full_path=source_file_full_path,
                            converted_file_full_path=converted_file_full_path,
                            translated_file_full_path=translated_file_full_path,
                            source_lang=task_result_content['source_lang'],
                            target_lang=task_result_content['target_lang'],
                            task_name=SpeechRecognitionTaskNameEnum.public_speech_translation.value
                        )

                        if isinstance(task_result, tuple):
                            task_result = task_result[0]

                        if isinstance(trans_history, tuple):
                            trans_history = trans_history[0]

                        update_request.append(
                            speech_recognition_request_repository.update(
                                task, 
                                dict(
                                    step_status=StepStatusEnum.completed.value,
                                    current_step=SpeechRecognitionTaskStepEnum.translating_speech.value
                                )
                            )
                        )
                        
                        update_request.append(
                            speech_recognition_history_repository.update(
                                trans_history, 
                                dict(
                                    status=SpeechRecognitionHistoryStatus.translated.value
                                )
                            )
                        )

                        update_request.append(
                            task_result.save_request_result_to_file(
                                content=new_saved_content.json()
                            )
                        )
                    
                    await asyncio.gather(*update_request)

            api_requests.append(
                contentTranslator.translate(
                    source_text=converted_text,
                    source_lang=source_lang,
                    target_lang=target_lang,
                    session=session,
                )
            )

        api_results = await asyncio.gather(*api_requests)

        async with db_instance.session() as session:

            async with session.start_transaction():
                
                update_request = []
                
                for task_id, api_result in zip(tasks_id, api_results):

                    task_result = valid_tasks_mapper[task_id]['task_result'],
                    recognize_history = valid_tasks_mapper[task_id]['recognize_history'],
                    task = valid_tasks_mapper[task_id]['task']
                    task_result_content = valid_tasks_mapper[task_id]['task_result_content']

                    translated_file_name = f'{get_speech_recognition_translated_file_name()}.txt'
                    translated_file_path = get_speech_recognition_file_path(task_id, translated_file_name)
                    translated_file_full_path = get_full_path(translated_file_path)

                    converted_file_full_path = task_result_content['converted_file_full_path']

                    with open(translated_file_full_path, "w+") as text_file:
                        text_file.write(api_result.data)

                    new_saved_content = SpeechRecognitionTask_TranslatedResultFileSchemaV1(
                        source_file_full_path=task_result_content['source_file_full_path'],
                        converted_file_full_path=converted_file_full_path,
                        translated_file_full_path=translated_file_full_path,
                        source_lang=task_result_content['source_lang'],
                        target_lang=task_result_content['target_lang'],
                        job_id=task_result_content['job_id'],
                        task_name=SpeechRecognitionTaskNameEnum.public_speech_translation.value
                    )

                    if isinstance(task_result, tuple):
                        task_result = task_result[0]

                    if isinstance(recognize_history, tuple):
                        recognize_history = recognize_history[0]

                    update_request.append(
                        speech_recognition_request_repository.update(
                            task, 
                            dict(
                                step_status=StepStatusEnum.completed.value,
                                current_step=SpeechRecognitionTaskStepEnum.translating_speech.value
                            )
                        )
                    )
                    
                    update_request.append(
                        speech_recognition_history_repository.update(
                            recognize_history, 
                            dict(
                                status=SpeechRecognitionHistoryStatus.translated.value
                            )
                        )
                    )

                    update_request.append(
                        task_result.save_request_result_to_file(
                            content=new_saved_content.json()
                        )
                    )                    
                
                await asyncio.gather(*update_request)
