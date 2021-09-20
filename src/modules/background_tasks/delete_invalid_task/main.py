from datetime import datetime

from uuid import UUID
from infrastructure.configs.main import GlobalConfig, get_cnf, get_mongodb_instance
from infrastructure.configs.task import (
    StepStatusEnum
)

from modules.translation_request.database.translation_request.repository import TranslationRequestRepository
from modules.task.database.task_result.repository import TasktResultRepository
from modules.task.database.task.repository import TaskRepository
from core.utils.common import chunk_arr

import asyncio
from infrastructure.adapters.logger import Logger

config: GlobalConfig = get_cnf()
db_instance = get_mongodb_instance()

translation_request_repository = TranslationRequestRepository()


logger = Logger('Task: delete_invalid_task')


async def main():

    logger.debug(
        msg=f'New task delete_invalid_task run in {datetime.now()}'
    )

    print(f'New task delete_invalid_task run in {datetime.now()}')

    from modules.task.database.task_result.repository import TasktResultRepository
    from modules.task.database.task.repository import TaskRepository

    task_repository = TaskRepository()

    task_result_repository = TasktResultRepository()

    try:

        expired_tasks = await translation_request_repository.find_many(
            params=dict(
                expired_date={
                    "$lt": datetime.now()
                }
            )
        )

        cancelled_tasks = await translation_request_repository.find_many(
            params=dict(
                step_status=StepStatusEnum.cancelled.value
            )
        )

        invalid_tasks_id = list(map(lambda task: task.id.value, expired_tasks + cancelled_tasks))

        if len(invalid_tasks_id) == 0:
            logger.debug(
                msg=f'An task delete_invalid_task end in {datetime.now()}\n')

            print(f'An task delete_invalid_task end in {datetime.now()}\n')
            return

        # for chunk in chunked_tasks_id:
        async with db_instance.session() as session:

            async with session.start_transaction():

                clean_request = []

                for task_id in (invalid_tasks_id):

                    clean_request.append(
                        task_repository.find(UUID(task_id).delete()))

                    clean_request.append(
                        task_result_repository.find(UUID(task_id).delete()))

                await asyncio.gather(*clean_request)

    except Exception as e:
        logger.error(e)

        print(e)

    logger.debug(
        msg=f'An task delete_invalid_task end in {datetime.now()}\n'
    )

    # print(f'An task translate_plain_text_in_public_request.detect_content_language end in {datetime.now()}\n')


# async def execute_in_batch(invalid_tasks_id):

   
