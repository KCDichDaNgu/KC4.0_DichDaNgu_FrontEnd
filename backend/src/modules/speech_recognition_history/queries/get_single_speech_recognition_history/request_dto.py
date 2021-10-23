from interface_adapters.interfaces.speech_recognition_request.get_single_speech_recognition_history import GetSingleSpeechRecognitionHistory
from sanic_openapi import doc

class GetSingleSpeechRecognitionHistoryRequestDto(GetSingleSpeechRecognitionHistory):

    taskId: doc.String(
        description='Task Id',
        name='taskId'
    )

    languageDetectionHistoryId: doc.String(
        description='SpeechRecognition History Id',
        required=False,
        name='languageDetectionHistoryId'
    )
    