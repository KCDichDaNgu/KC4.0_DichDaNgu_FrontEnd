from modules.translation_request.domain.entities.translation_history import TranslationHistoryProps

from modules.translation_request.domain.services.translation_request_service import TranslationRequestDService
from modules.translation_request.commands.create_file_translation_request.command import CreateFileTranslationRequestCommand

class CreateFileTranslationRequestService():

    def __init__(self) -> None:
        
        self.__translationRequestDService = TranslationRequestDService()

    async def create_request(self, command: CreateFileTranslationRequestCommand):

        return await self.__translationRequestDService.create_file_translation_request(command=command)
