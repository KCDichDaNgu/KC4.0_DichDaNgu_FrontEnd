from infrastructure.configs.language import LanguageEnum
from modules.translation_request.domain.entities.translation_history import TranslationHistoryProps
from core.value_objects import ID
from infrastructure.configs.task import (
    CreatorTypeEnum, 
    StepStatusEnum, 
    TranslationTaskNameEnum, 
    TranslationTaskStepEnum,
    TranslationTask_NotYetTranslatedResultFileSchemaV1, 
    TranslationTask_LangUnknownResultFileSchemaV1
)
from modules.translation_request.database.translation_request.repository import (
    TranslationRequestRepository, TranslationRequestRepositoryPort
)
from modules.translation_request.commands.create_plain_text_translation_request.command import CreatePlainTextTranslationRequestCommand
from modules.translation_request.domain.entities.translation_request import TranslationRequestEntity, TranslationRequestProps 
from modules.translation_request.domain.entities.translation_request_result import TranslationRequestResultProps
from modules.translation_request.database.translation_request_result.repository import (
    TranslationRequestResultRepository, 
    TranslationRequestResultEntity,
    TranslationRequestResultRepositoryPort
)
from modules.translation_request.database.translation_history.repository import (
    TranslationHistoryEntity,
    TranslationHistoryRepositoryPort,
    TranslationHistoryRepository
)

from infrastructure.configs.translation_history import TranslationHistoryTypeEnum, TranslationHistoryStatus
from infrastructure.configs.main import get_mongodb_instance
from modules.translation_request.commands.create_file_translation_request.command import CreateFileTranslationRequestCommand
from infrastructure.configs.translation_task import FileTranslationTask_LangUnknownResultFileSchemaV1, FileTranslationTask_NotYetTranslatedResultFileSchemaV1

import io

TEXT_TRANSLATION_TASKS = [
    TranslationTaskNameEnum.private_plain_text_translation.value, 
    TranslationTaskNameEnum.public_plain_text_translation
]

class TranslationRequestDService():

    def __init__(self) -> None:
        
        self.__translation_request_repository: TranslationRequestRepositoryPort = TranslationRequestRepository()
        self.__translation_request_result_repository : TranslationRequestResultRepositoryPort = TranslationRequestResultRepository()
        self.__translation_history_repository: TranslationHistoryRepositoryPort = TranslationHistoryRepository()
        self.__db_instance = get_mongodb_instance()

    async def create(self, command: CreatePlainTextTranslationRequestCommand):

        if command.source_lang in LanguageEnum.enum_values():

            begin_step = TranslationTaskStepEnum.translating_language.value

            saved_content = TranslationTask_NotYetTranslatedResultFileSchemaV1(
                source_text=command.source_text,
                source_lang=command.source_lang,
                target_lang=command.target_lang,
                task_name=TranslationTaskNameEnum.private_plain_text_translation.value
            )

        else:
            
            begin_step = TranslationTaskStepEnum.detecting_language.value

            saved_content = TranslationTask_LangUnknownResultFileSchemaV1(
                source_text=command.source_text,
                target_lang=command.target_lang,
                task_name=TranslationTaskNameEnum.public_plain_text_translation.value
            )
            
        new_request = TranslationRequestEntity(
            TranslationRequestProps(
                creator_id=ID(None),
                creator_type=CreatorTypeEnum.end_user.value,
                task_name=TranslationTaskNameEnum.public_plain_text_translation.value,
                step_status=StepStatusEnum.not_yet_processed.value,
                current_step=begin_step
            )
        )
        
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
            
            async with self.__db_instance.session() as session:
                async with session.start_transaction():

                    created_request = await self.__translation_request_repository.create(
                        new_request
                    )

                    await self.__translation_request_result_repository.create(
                        new_task_result_entity
                    )
                    
                    created_translation_record = await self.__translation_history_repository.create(
                        new_translation_history_entity
                    )
                    
                    return created_request, created_translation_record

    async def create_file_translation_request(self, command: CreateFileTranslationRequestCommand):

        if command.source_lang in LanguageEnum.enum_values():
            begin_step = TranslationTaskStepEnum.translating_language.value
        else:
            begin_step = TranslationTaskStepEnum.detecting_language.value
        
        new_request = TranslationRequestEntity(
            TranslationRequestProps(
                creator_id=ID(None),
                creator_type=CreatorTypeEnum.end_user.value,
                task_name=TranslationTaskNameEnum.public_file_translation.value,
                step_status=StepStatusEnum.not_yet_processed.value,
                current_step=begin_step
            )
        )
        
        new_task_result_entity = TranslationRequestResultEntity(
            TranslationRequestResultProps(
                task_id=new_request.id,
                step=new_request.props.current_step
            )
        )  

        # source_file_name = gen_file_translation_source_file_path(new_task_result_entity.props.task_id.value)

        # saved_file_path = save_object_to_binary_file(source_file_name, command.source_file)

        # if command.source_lang in LanguageEnum.enum_values():

        #     saved_content = FileTranslationTask_NotYetTranslatedResultFileSchemaV1(
        #         source_file_path=saved_file_path,
        #         source_lang=command.source_lang,
        #         target_lang=command.target_lang,
        #         task_name=TranslationTaskNameEnum.private_file_translation.value
        #     )

        # else:

        #     saved_content = FileTranslationTask_LangUnknownResultFileSchemaV1(
        #         source_file_path=saved_file_path,
        #         target_lang=command.target_lang,
        #         task_name=TranslationTaskNameEnum.public_file_translation.value
        #     )

        # saving_content_result = await new_task_result_entity.save_request_result_to_file(
        #     content=saved_content.json()
        # )

        # if saving_content_result:
        
        #     new_translation_history_entity = TranslationHistoryEntity(
        #         TranslationHistoryProps(
        #             creator_id=new_request.props.creator_id,
        #             task_id=new_request.id,
        #             translation_type=TranslationHistoryTypeEnum.public_file_translation.value,
        #             status=TranslationHistoryStatus.translating.value,
        #             file_path=new_task_result_entity.props.file_path
        #         )
        #     )
            
        #     async with self.__db_instance.session() as session:
        #         async with session.start_transaction():

        #             created_request = await self.__translation_request_repository.create(
        #                 new_request
        #             )

        #             await self.__translation_request_result_repository.create(
        #                 new_task_result_entity
        #             )
                    
        #             created_translation_record = await self.__translation_history_repository.create(
        #                 new_translation_history_entity
        #             )
                    
        #             return created_request, created_translation_record
