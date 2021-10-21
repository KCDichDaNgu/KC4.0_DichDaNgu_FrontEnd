from infrastructure.configs.speech_recognition_task import SpeechRecognitionTaskNameEnum
from infrastructure.configs.task import SpeechRecognitionTaskNameEnum
from interface_adapters.base_classes.response import ResponseBase
from sanic_openapi import doc
from infrastructure.configs.speech_recognition_history import SpeechRecognitionHistoryStatus

class DataStructure:

    taskId = doc.String(required=True)

    speechRecognitionType = doc.String(
        required=True,
        choices=SpeechRecognitionTaskNameEnum.enum_values()
    )

    status = doc.String(
        required=True,
        choices=SpeechRecognitionHistoryStatus.enum_values()
    )

    resultUrl = doc.String(
        required=True
    )

    id = doc.String(
        required=True,
        choices=SpeechRecognitionTaskNameEnum.enum_values()
    )

    updatedAt = doc.DateTime(
        required=True,
    )

    createdAt = doc.DateTime(
        required=True,
    )

class SingleSpeechRecognitionHistoryResponse(ResponseBase):
    
    data: DataStructure
