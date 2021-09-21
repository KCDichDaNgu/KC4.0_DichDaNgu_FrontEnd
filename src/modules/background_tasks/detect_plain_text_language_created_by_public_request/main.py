from datetime import datetime
from infrastructure.configs.language_detection_history import LanguageDetectionHistoryStatus
from core.utils.common import chunk_arr


from typing import List
from uuid import UUID

from infrastructure.configs.main import GlobalConfig, get_cnf, get_mongodb_instance
from infrastructure.configs.task import (
    LanguageDetectionTask_LangUnknownResultFileSchemaV1, 
    LanguageDetectionTask_LanguageDetectionCompletedResultFileSchemaV1,
    LanguageDetectionTaskNameEnum, 
    LanguageDetectionTaskStepEnum, 
    StepStatusEnum
)

from infrastructure.adapters.language_detector.main import LanguageDetector

from modules.language_detection_request.database.language_detection_request.repository import LanguageDetectionRequestRepository, LanguageDetectionRequestEntity
from modules.language_detection_request.database.language_detection_request_result.repository import LanguageDetectionRequestResultRepository, LanguageDetectionRequestResultEntity
from modules.language_detection_request.database.language_detection_history.repository import LanguageDetectionHistoryRepository, LanguageDetectionHistoryEntity

import asyncio
import aiohttp

from infrastructure.adapters.logger import Logger

config: GlobalConfig = get_cnf()
db_instance = get_mongodb_instance()

PUBLIC_LANGUAGE_DETECTION_API_CONF = config.PUBLIC_LANGUAGE_DETECTION_API
ALLOWED_CONCURRENT_REQUEST = PUBLIC_LANGUAGE_DETECTION_API_CONF.ALLOWED_CONCURRENT_REQUEST

language_detection_request_repository = LanguageDetectionRequestRepository()
language_detection_request_result_repository = LanguageDetectionRequestResultRepository()
language_detection_history = LanguageDetectionHistoryRepository()

languageDetector = LanguageDetector()

logger = Logger('Task: translate_plain_text_in_public_request.detect_content_language')

async def read_task_result(
    tasks_result: List[LanguageDetectionRequestResultEntity], 
    tasks: List[LanguageDetectionRequestEntity],
    language_detections_history: List[LanguageDetectionHistoryEntity]
):
    
    valid_tasks_mapper = {}

    task_id_1 = list(map(lambda t: t.id.value, tasks))
    task_id_2 = list(map(lambda ts: ts.props.task_id.value, tasks_result))
    task_id_3 = list(map(lambda th: th.props.task_id.value, language_detections_history))

    intersection_tasks_id = list(set(task_id_1) & set(task_id_2) & set(task_id_3))
    
    for task_id in intersection_tasks_id:

        task = list(filter(lambda ts: ts.id.value == task_id, tasks))[0]
        task_result = list(filter(lambda ts: ts.props.task_id.value == task_id, tasks_result))[0]
        trans_history = list(filter(lambda ts: ts.props.task_id.value == task_id, language_detections_history))[0]

        try: 
            data = await task_result.read_data_from_file()
            
            if data['status'] == LanguageDetectionTask_LangUnknownResultFileSchemaV1(
                source_text='',
                task_name=LanguageDetectionTaskNameEnum.public_plain_text_language_detection.value
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

    invalid_tasks_id = list(map(lambda t: t.id.value, invalid_tasks))

    invalid_tasks_mapper = {}

    for task_id in invalid_tasks_id:

        task = list(filter(lambda ts: ts.id.value == task_id, tasks))[0]
        task_result = list(filter(lambda ts: ts.props.task_id.value == task_id, tasks_result))[0]
        trans_history = list(filter(lambda ts: ts.props.task_id.value == task_id, language_detections_history))[0]

        invalid_tasks_mapper[task_id] = {
            'task_result': task_result,
            'trans_history': trans_history,
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
                trans_history = invalid_tasks_mapper[task_id]['trans_history'],
                task = invalid_tasks_mapper[task_id]['task']

                if isinstance(task_result, tuple):
                    task_result = task_result[0]

                if isinstance(trans_history, tuple):
                    trans_history = trans_history[0]
                    
                update_request.append(
                    language_detection_request_repository.update(
                        task, 
                        dict(step_status=StepStatusEnum.cancelled.value),
                        conditions={}
                    )
                )
                
                update_request.append(
                    language_detection_history.update(
                        trans_history, 
                        dict(
                            status=LanguageDetectionHistoryStatus.cancelled.value
                        )
                    )
                )
                
            result = await asyncio.gather(*update_request)

    return result

async def main():

    logger.debug(
        msg=f'New task translate_plain_text_in_public_request.detect_content_language run in {datetime.now()}'
    )

    print(f'New task translate_plain_text_in_public_request.detect_content_language run in {datetime.now()}')
    
    try:
        
        tasks = await language_detection_request_repository.find_many(
            params=dict(
                task_name=LanguageDetectionTaskNameEnum.public_plain_text_language_detection.value,
                current_step=LanguageDetectionTaskStepEnum.detecting_language.value,
                step_status=StepStatusEnum.not_yet_processed.value,
                expired_date={
                    "$gt": datetime.now()
                }
            ),
            limit=ALLOWED_CONCURRENT_REQUEST * 10
        )

        tasks_id = list(map(lambda task: task.id.value, tasks))

        if len(tasks_id) == 0: 
            logger.debug(
                msg=f'An task translate_plain_text_in_public_request.detect_content_language end in {datetime.now()}\n'
            )

            print(f'An task translate_plain_text_in_public_request.detect_content_language end in {datetime.now()}\n')
            return

        tasks_result_and_trans_history_req = [
            language_detection_request_result_repository.find_many(
                params=dict(
                    task_id={
                        '$in': list(map(lambda t: UUID(t), tasks_id))
                    },
                    step=LanguageDetectionTaskStepEnum.detecting_language.value
                )
            ),
            language_detection_history.find_many(
                params=dict(
                    task_id={
                        '$in': list(map(lambda t: UUID(t), tasks_id))
                    }
                )
            )
        ]

        tasks_result, language_detections_history = await asyncio.gather(*tasks_result_and_trans_history_req)
    
        valid_tasks_mapper, invalid_tasks_mapper = await read_task_result(
            tasks=tasks, 
            tasks_result=tasks_result,
            language_detections_history=language_detections_history
        )

        await mark_invalid_tasks(invalid_tasks_mapper)
        
        valid_tasks_id = list(map(lambda t: t.id.value, tasks))

        chunked_tasks_id = list(chunk_arr(valid_tasks_id, ALLOWED_CONCURRENT_REQUEST))

        for chunk in chunked_tasks_id:

            try:
            
                await execute_in_batch(valid_tasks_mapper, chunk)
                
            except Exception as e:
                logger.error(e)
                
                print(e)

    except Exception as e:
        logger.error(e)
        
        print(e)

    logger.debug(
        msg=f'An task translate_plain_text_in_public_request.detect_content_language end in {datetime.now()}\n'
    )

    print(f'An task translate_plain_text_in_public_request.detect_content_language end in {datetime.now()}\n')
            

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
        
        async with db_instance.session() as session:

            async with session.start_transaction():
    
                update_request = []

                for task_id, api_result in zip(tasks_id, api_results):

                    task_result = valid_tasks_mapper[task_id]['task_result'],
                    trans_history = valid_tasks_mapper[task_id]['trans_history'],
                    task = valid_tasks_mapper[task_id]['task']
                    task_result_content = valid_tasks_mapper[task_id]['task_result_content']
                    
                    new_saved_content = LanguageDetectionTask_LanguageDetectionCompletedResultFileSchemaV1(
                        source_text=task_result_content['source_text'],
                        source_lang=api_result.lang,
                        task_name=LanguageDetectionTaskNameEnum.public_plain_text_language_detection.value
                    )

                    if isinstance(task_result, tuple):
                        task_result = task_result[0]

                    if isinstance(trans_history, tuple):
                        trans_history = trans_history[0]
                
                    update_request.append(
                        language_detection_request_repository.update(
                            task, 
                            dict(
                                step_status=StepStatusEnum.completed.value
                            )
                        )
                    )
                    
                    update_request.append(
                        language_detection_history.update(
                            trans_history, 
                            dict(
                                status=LanguageDetectionHistoryStatus.detected.value
                            )
                        )
                    )

                    update_request.append(
                        task_result.save_request_result_to_file(
                            content=new_saved_content.json()
                        )
                    )

                await asyncio.gather(*update_request)
