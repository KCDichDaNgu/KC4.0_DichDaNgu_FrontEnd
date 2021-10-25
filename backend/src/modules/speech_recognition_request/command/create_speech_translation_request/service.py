from modules.speech_recognition_request.command.create_speech_translation_request.command import CreateSpeechTranslationRequestCommand

from modules.speech_recognition_request.domain.services.speech_recognition_request_service import SpeechRecognitionRequestDService

class CreateSpeechTranslationRequestService():

    def __init__(self) -> None:
        
        self.__speech_recognition_request_d_service = SpeechRecognitionRequestDService()

    async def create_request(self, command: CreateSpeechTranslationRequestCommand):
        return await self.__speech_recognition_request_d_service.create_translation_request(command=command)
