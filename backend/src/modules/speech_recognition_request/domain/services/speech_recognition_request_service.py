from infrastructure.configs.main import get_mongodb_instance
from infrastructure.configs.speech_recognition_history import (
    SpeechRecognitionHistoryTypeEnum,
    SpeechRecognitionHistoryStatus,
)
from infrastructure.configs.speech_recognition_task import SpeechRecognitionTask_NotYetConvertedResultFileSchemaV1, SpeechRecognitionTaskNameEnum
from modules.speech_recognition_request.command.create_speech_translation_request.command import CreateSpeechTranslationRequestCommand
from modules.speech_recognition_request.domain.entities.speech_recognition_history import SpeechRecognitionHistoryEntity, SpeechRecognitionHistoryProps
from modules.speech_recognition_request.command.create_speech_recognition_request.command import CreateSpeechRecognitionRequestCommand
from modules.speech_recognition_request.database.speech_recognition_history.repository import SpeechRecognitionHistoryRepository, SpeechRecognitionHistoryRepositoryPort
from modules.speech_recognition_request.database.speech_recognition_request_result.repository import SpeechRecognitionRequestResultRepository, SpeechRecognitionRequestResultRepositoryPort
from modules.speech_recognition_request.database.speech_recognition_request.repository import SpeechRecognitionRequestRepository, SpeechRecognitionRequestRepositoryPort
from infrastructure.configs.task import CreatorTypeEnum, SpeechRecognitionTaskStepEnum, StepStatusEnum
from modules.speech_recognition_request.domain.entities.speech_recognition_request import SpeechRecognitionRequestEntity, SpeechRecognitionRequestProps
from modules.speech_recognition_request.domain.entities.speech_recognition_request_result import SpeechRecognitionRequestResultEntity, SpeechRecognitionRequestResultProps

class SpeechRecognitionRequestDService():
    def __init__(self) -> None:
        self.__speech_recognition_request_repository: SpeechRecognitionRequestRepositoryPort = SpeechRecognitionRequestRepository()
        self.__speech_recognition_request_result_repository : SpeechRecognitionRequestResultRepositoryPort = SpeechRecognitionRequestResultRepository()
        self.__speech_recognition_history_repository: SpeechRecognitionHistoryRepositoryPort = SpeechRecognitionHistoryRepository()
        self.__db_instance = get_mongodb_instance()

    async def create_conversion_request(self, command: CreateSpeechRecognitionRequestCommand):
        begin_step = SpeechRecognitionTaskStepEnum.converting_speech.value

        new_request = SpeechRecognitionRequestEntity(
            SpeechRecognitionRequestProps(
                creator_id=command.creator_id,
                creator_type=CreatorTypeEnum.end_user.value,
                task_name=SpeechRecognitionTaskNameEnum.public_speech_recognition.value,
                step_status=StepStatusEnum.not_yet_processed.value,
                current_step=begin_step
            )
        )

        new_task_result_entity = SpeechRecognitionRequestResultEntity(
            SpeechRecognitionRequestResultProps(
                task_id=new_request.id,
                step=new_request.props.current_step,
            )
        )  

        create_file_result = await new_task_result_entity.create_required_files_for_speech_recognition_task(command.source_file)

        saved_content = SpeechRecognitionTask_NotYetConvertedResultFileSchemaV1(
            source_file_full_path=create_file_result.data['source_file_full_path'],
            source_lang=command.source_lang,
            task_name=SpeechRecognitionTaskNameEnum.public_speech_recognition.value
        )

        saving_content_result = await new_task_result_entity.save_request_result_to_file(
            content=saved_content.json()
        )

        if saving_content_result:
        
            new_speech_recognition_history_entity = SpeechRecognitionHistoryEntity(
                SpeechRecognitionHistoryProps(
                    creator_id=new_request.props.creator_id,
                    task_id=new_request.id,
                    speech_recognition_type=SpeechRecognitionHistoryTypeEnum.public_speech_recognition.value,
                    status=SpeechRecognitionHistoryStatus.converting.value,
                    file_path=new_task_result_entity.props.file_path
                )
            )
            
            async with self.__db_instance.session() as session:
                async with session.start_transaction():

                    created_request = await self.__speech_recognition_request_repository.create(
                        new_request
                    )

                    await self.__speech_recognition_request_result_repository.create(
                        new_task_result_entity
                    )
                    
                    created_speech_recognition_record = await self.__speech_recognition_history_repository.create(
                        new_speech_recognition_history_entity
                    )
                    
                    return created_request, created_speech_recognition_record

    async def create_translation_request(self, command: CreateSpeechTranslationRequestCommand):
        begin_step = SpeechRecognitionTaskStepEnum.converting_speech.value

        new_request = SpeechRecognitionRequestEntity(
            SpeechRecognitionRequestProps(
                creator_id=command.creator_id,
                creator_type=CreatorTypeEnum.end_user.value,
                task_name=SpeechRecognitionTaskNameEnum.public_speech_translation.value,
                step_status=StepStatusEnum.not_yet_processed.value,
                current_step=begin_step
            )
        )

        new_task_result_entity = SpeechRecognitionRequestResultEntity(
            SpeechRecognitionRequestResultProps(
                task_id=new_request.id,
                step=new_request.props.current_step,
            )
        )  

        create_file_result = await new_task_result_entity.create_required_files_for_speech_recognition_task(command.source_file)

        saved_content = SpeechRecognitionTask_NotYetConvertedResultFileSchemaV1(
            source_file_full_path=create_file_result.data['source_file_full_path'],
            source_lang=command.source_lang,
            target_lang=command.target_lang,
            task_name=SpeechRecognitionTaskNameEnum.public_speech_translation.value
        )

        saving_content_result = await new_task_result_entity.save_request_result_to_file(
            content=saved_content.json()
        )

        if saving_content_result:
        
            new_speech_recognition_history_entity = SpeechRecognitionHistoryEntity(
                SpeechRecognitionHistoryProps(
                    creator_id=new_request.props.creator_id,
                    task_id=new_request.id,
                    speech_recognition_type=SpeechRecognitionHistoryTypeEnum.public_speech_translation.value,
                    status=SpeechRecognitionHistoryStatus.converting.value,
                    file_path=new_task_result_entity.props.file_path
                )
            )
            
            async with self.__db_instance.session() as session:
                async with session.start_transaction():

                    created_request = await self.__speech_recognition_request_repository.create(
                        new_request
                    )

                    await self.__speech_recognition_request_result_repository.create(
                        new_task_result_entity
                    )
                    
                    created_speech_recognition_record = await self.__speech_recognition_history_repository.create(
                        new_speech_recognition_history_entity
                    )
                    print(created_speech_recognition_record)
                    return created_request, created_speech_recognition_record