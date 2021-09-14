from modules.translation_request.domain.entities.translation_history import TranslationHistoryProps
from cassandra.cqlengine.query import BatchQuery
from core.value_objects import ID
from infrastructure.configs.translation_request import CreatorTypeEnum, StatusEnum, TaskTypeEnum, TranslationStepEnum
from modules.translation_request.database.translation_request.repository import (
    TranslationRequestRepository, TranslationRequestRepositoryPort
)
from modules.translation_request.commands.create_plain_text_translation_request.command import CreatePlainTextTranslationRequestCommand
from modules.translation_request.domain.entities.translation_request import TranslationRequestEntity, TranslationRequestProps 
from modules.translation_request.domain.entities.translation_request_result import TranslationRequestResultProps
from modules.translation_request.database.translation_request_result.repository import (
    TranslationRequestResultRepository, 
    TranslationRequestResultEntity
)
from modules.translation_request.database.translation_history.repository import (
    TranslationHistoryEntity,
    TranslationHistoryRepositoryPort,
    TranslationHistoryRepository
)

from infrastructure.configs.translation_history import TranslationHistoryTypeEnum, TranslationHistoryStatus

TEXT_TRANSLATION_TASKS = [
    TaskTypeEnum.plain_text_translation.value, 
    TaskTypeEnum.public_plain_text_translation
]

class CreatePlainTextTranslationRequestService():

    def __init__(self) -> None:
        
        self.__translation_request_repository: TranslationRequestRepositoryPort = TranslationRequestRepository()
        self.__translation_request_result_repository : TranslationRequestRepositoryPort = TranslationRequestResultRepository()
        self.__translation_history_repository: TranslationHistoryRepositoryPort = TranslationHistoryRepository()

    async def create_request(self, command: CreatePlainTextTranslationRequestCommand):

        new_request = TranslationRequestEntity(
            TranslationRequestProps(
                creator_id=ID(None),
                creator_type=CreatorTypeEnum.end_user.value,
                task_type=TaskTypeEnum.public_plain_text_translation.value,
                status=StatusEnum.not_yet_processed.value,
                current_step=TranslationStepEnum.detecting_language.value
            )
        )
        
        new_task_result_entity = TranslationRequestResultEntity(
            TranslationRequestResultProps(
                task_id=new_request.id,
                step=new_request.props.current_step
            )
        )

        await new_task_result_entity.save_request_result_to_file(content=command.json())

        new_translation_history_entity = TranslationHistoryEntity(
            TranslationHistoryProps(
                creator_id=new_request.props.creator_id,
                task_id=new_request.id,
                translation_type=TranslationHistoryTypeEnum.public_plain_text_translation.value,
                status=TranslationHistoryStatus.translating.value,
                file_path=new_task_result_entity.props.file_path
            )
        )

        b = BatchQuery()

        created = await self.__translation_request_repository.create(
            new_request, 
            b
        )

        await self.__translation_request_result_repository.create(
            new_task_result_entity,
            b
        )

        await self.__translation_history_repository.create(
            new_translation_history_entity,
            b
        )

        b.execute()
        
        return created
