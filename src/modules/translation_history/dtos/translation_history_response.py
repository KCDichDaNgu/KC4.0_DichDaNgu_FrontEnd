from infrastructure.configs.task import TranslationTaskNameEnum
from interface_adapters.base_classes.response import ResponseBase
from sanic_openapi import doc
from infrastructure.configs.translation_history import TranslationHistoryStatus

class DataStructure:

    taskId = doc.String(required=True)

    translationType = doc.String(
        required=True,
        choices=TranslationTaskNameEnum.enum_values()
    )

    status = doc.String(
        required=True,
        choices=TranslationHistoryStatus.enum_values()
    )

    result_url = doc.String(
        required=True
    )

    id = doc.String(
        required=True,
        choices=TranslationTaskNameEnum.enum_values()
    )

    updatedAt = doc.DateTime(
        required=True,
    )

    createdAt = doc.DateTime(
        required=True,
    )

class SingleTranslationHistoryResponse(ResponseBase):
    
    data: DataStructure
