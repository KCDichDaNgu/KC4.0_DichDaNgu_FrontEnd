from modules.speech_recognition_request.domain.entities.speech_recognition_history import SpeechRecognitionHistoryProps

from modules.speech_recognition_request.domain.services.speech_recognition_request_service import SpeechRecognitionRequestDService
from modules.speech_recognition_request.command.create_speech_recognition_request.command import CreateSpeechRecognitionRequestCommand

class CreateSpeechRecognitionRequestService():

    def __init__(self) -> None:
        
        self.__speech_recognition_request_d_service = SpeechRecognitionRequestDService()

    async def create_request(self, command: CreateSpeechRecognitionRequestCommand):
        return await self.__speech_recognition_request_d_service.create_conversion_request(command=command)
