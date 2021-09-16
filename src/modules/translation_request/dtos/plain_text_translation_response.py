from infrastructure.configs.translation_request import TaskTypeEnum
from interface_adapters.base_classes.response import ResponseBase
from sanic_openapi import doc

class DataStructure:

    taskId = doc.String(required=True)

    taskType = doc.String(
        required=True,
        choices=TaskTypeEnum.enum_values()
    )

    translationHistoryId = doc.String(
        required=True
    )

class PlainTextTranslationRequestResponse(ResponseBase):
    
    data: DataStructure
