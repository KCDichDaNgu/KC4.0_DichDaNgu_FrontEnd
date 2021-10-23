from pydantic.types import FilePath
from infrastructure.configs.translation_history import TranslationHistoryStatus
from infrastructure.configs.translation_request import TaskTypeEnum
from pydantic import BaseModel
from interface_adapters.base_classes.response import ResponseBase
from sanic_openapi import doc


class DataStructure:

    taskId = doc.String(required=True)
    status = doc.String(
        required=True)

    translationType = doc.String(
        required=True,
        choices=TaskTypeEnum.enum_values()
    )

    filePath = doc.String(required=True)


class TranslationHistoryResponse(ResponseBase):

    data: DataStructure
