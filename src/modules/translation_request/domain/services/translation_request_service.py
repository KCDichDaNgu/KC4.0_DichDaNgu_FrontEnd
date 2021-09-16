from infrastructure.configs.language import LanguageEnum
from modules.translation_request.domain.entities.translation_history import TranslationHistoryProps
from core.value_objects import ID
from infrastructure.configs.translation_request import (
    CreatorTypeEnum, StepStatusEnum, TaskTypeEnum, TranslationStepEnum,
    NotYetTranslatedResultFileSchemaV1, LanguageNotYetDetectedResultFileSchemaV1
)
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
from infrastructure.configs.main import get_mongodb_instance

TEXT_TRANSLATION_TASKS = [
    TaskTypeEnum.plain_text_translation.value, 
    TaskTypeEnum.public_plain_text_translation
]

class TranslationRequestDService():

    def __init__(self) -> None:
        
        self.__translation_request_repository: TranslationRequestRepositoryPort = TranslationRequestRepository()
        self.__translation_request_result_repository : TranslationRequestRepositoryPort = TranslationRequestResultRepository()
        self.__translation_history_repository: TranslationHistoryRepositoryPort = TranslationHistoryRepository()
        self.__db_instance = get_mongodb_instance()

    async def create(self, command: CreatePlainTextTranslationRequestCommand):

        if command.source_lang in LanguageEnum.enum_values():

            begin_step = TranslationStepEnum.translating_language.value

            saved_content = NotYetTranslatedResultFileSchemaV1(
                source_text=command.source_text,
                source_lang=command.source_lang,
                target_lang=command.target_lang,
            )

        else:
            
            begin_step = TranslationStepEnum.detecting_language.value

            saved_content = LanguageNotYetDetectedResultFileSchemaV1(
                source_text=command.source_text,
                target_lang=command.target_lang,
            )
            
        new_request = TranslationRequestEntity(
            TranslationRequestProps(
                creator_id=ID(None),
                creator_type=CreatorTypeEnum.end_user.value,
                task_type=TaskTypeEnum.public_plain_text_translation.value,
                step_status=StepStatusEnum.not_yet_processed.value,
                current_step=begin_step
            )
        )
        print(new_request)
        new_task_result_entity = TranslationRequestResultEntity(
            TranslationRequestResultProps(
                task_id=new_request.id,
                step=new_request.props.current_step
            )
        )

        saving_content_result = await new_task_result_entity.save_request_result_to_file(
            content=saved_content.json()
        )

        if saving_content_result:
        
            new_translation_history_entity = TranslationHistoryEntity(
                TranslationHistoryProps(
                    creator_id=new_request.props.creator_id,
                    task_id=new_request.id,
                    translation_type=TranslationHistoryTypeEnum.public_plain_text_translation.value,
                    status=TranslationHistoryStatus.translating.value,
                    file_path=new_task_result_entity.props.file_path
                )
            )
            
            with self.__db_instance.session() as session:
                with session.start_transaction():

                    created = await self.__translation_request_repository.create(
                        new_request
                    )

                    await self.__translation_request_result_repository.create(
                        new_task_result_entity
                    )
                    
                    await self.__translation_history_repository.create(
                        new_translation_history_entity
                    )
                    
                    return created
