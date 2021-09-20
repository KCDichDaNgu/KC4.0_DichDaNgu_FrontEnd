from modules.translation_request.domain.entities.translation_history import TranslationHistoryProps

from modules.translation_request.commands.create_plain_text_translation_request.command import CreatePlainTextTranslationRequestCommand
from modules.translation_request.domain.services.translation_request_service import TranslationRequestDService

class CreatePlainTextTranslationRequestService():

    def __init__(self) -> None:
        
        self.__translationRequestDService = TranslationRequestDService()

    async def create_request(self, command: CreatePlainTextTranslationRequestCommand):

        return await self.__translationRequestDService.create(command=command)
