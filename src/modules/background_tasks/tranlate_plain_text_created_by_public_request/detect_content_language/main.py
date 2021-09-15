from datetime import datetime

from modules.translation_request.domain.entities.translation_request_result import TranslationRequestResultEntity
from typing import List
from uuid import UUID

from infrastructure.configs.main import GlobalConfig, get_cnf, get_mongodb_instance
from infrastructure.configs.translation_request import (
    TaskTypeEnum, TranslationStepEnum, StepStatusEnum
)

from infrastructure.adapters.language_detector.main import LanguageDetector
from modules.translation_request.database.translation_request.repository import TranslationRequestRepository
from modules.translation_request.database.translation_request_result.repository import TranslationRequestResultRepository

import asyncio
import aiohttp

config: GlobalConfig = get_cnf()
db_instance = get_mongodb_instance()

PUBLIC_LANGUAGE_DETECTION_API_CONF = config.PUBLIC_LANGUAGE_DETECTION_API
ALLOWED_CONCURRENT_REQUEST = PUBLIC_LANGUAGE_DETECTION_API_CONF.ALLOWED_CONCURRENT_REQUEST
LANGUAGE_DETECTION_API_URL = PUBLIC_LANGUAGE_DETECTION_API_CONF.URL

translationRequestRepository = TranslationRequestRepository()
translationRequestResultRepository = TranslationRequestResultRepository()

async def read_task_result(tasks_result: List[TranslationRequestResultEntity]):
    
    invalid_task_ids = []
    task_id_task_result_content = {}

    for task_result in tasks_result:

        task_id = task_result.props['task_id'].value

        try: 
            data = await task_result.read_data_from_file()

            task_id_task_result_content[task_id] = data
        except Exception as e:
            print(e)
            invalid_task_ids.append(task_id)

    return task_id_task_result_content, invalid_task_ids

async def mark_invalid_tasks(invalid_tasks_id):
    pass

async def main():
    
    connector = aiohttp.TCPConnector(limit=ALLOWED_CONCURRENT_REQUEST)

    now = datetime.now()
    
    async with aiohttp.ClientSession(connector=connector) as session:

        tasks = await translationRequestRepository.find_many(
            params=dict(
                task_type=TaskTypeEnum.public_plain_text_translation.value,
                current_step=TranslationStepEnum.detecting_language.value,
                step_status=StepStatusEnum.not_yet_processed.value,
                expired_date={
                    "$gt": now
                }
            ),
            limit=ALLOWED_CONCURRENT_REQUEST
        )

        tasks_id = list(map(lambda task: task.id.value, tasks))
        
        tasks_result = await translationRequestResultRepository.find_many(
            params=dict(
                task_id={
                    '$in': list(map(lambda t: UUID(t), tasks_id))
                },
                step=TranslationStepEnum.detecting_language.value
            ),
            limit=ALLOWED_CONCURRENT_REQUEST
        )
        print(len(tasks_result))
        task_id_task_result_content, invalid_task_ids = await read_task_result(tasks_result)
        print(invalid_task_ids)
        await mark_invalid_tasks(invalid_task_ids)

        api_requests = []

        for task_id in task_id_task_result_content.keys():

            api_requests.append(
                LanguageDetector.detect(
                    url=LANGUAGE_DETECTION_API_URL, 
                    text=task_id_task_result_content[task_id], 
                    session=session
                )
            )

        api_results = await asyncio.gather(*api_requests)
        
        # async with db_instance.session() as session:
        #     print(api_results)
