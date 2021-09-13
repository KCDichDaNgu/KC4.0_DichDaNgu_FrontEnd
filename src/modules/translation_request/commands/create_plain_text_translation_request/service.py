from core.value_objects import DateVO
from infrastructure.configs.translation_request import CreatorTypeEnum, StatusEnum, TaskTypeEnum, TranslationStepEnum
from modules.translation_request.database.translation_request.repository import TranslationRequestRepository
from modules.translation_request.database import TranslationRequestRepositoryPort
from modules.translation_request.commands.create_plain_text_translation_request.command import CreatePlainTextTranslationRequestCommand
from modules.translation_request.domain.entities.translation_request import TranslationRequestEntity, TranslationRequestProps 

class CreatePlainTextTranslationRequestService():

    def __init__(self) -> None:
        
        self.__translation_request_repository: TranslationRequestRepositoryPort = TranslationRequestRepository()

    async def create_request(self, command: CreatePlainTextTranslationRequestCommand):

        new_request = TranslationRequestEntity(
            TranslationRequestProps(**{
                'creator_type': CreatorTypeEnum.end_user.value,
                'task_type': TaskTypeEnum.public_plain_text_translation.value,
                'status': StatusEnum.not_yet_processed.value,
                'current_step': TranslationStepEnum.detecting_language.value,
                'expired_date': DateVO.now()
            })
        )
        
        created = await self.__translation_request_repository.save(new_request)

        return created

