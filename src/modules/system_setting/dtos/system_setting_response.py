from infrastructure.configs.task import TaskTypeEnum
from pydantic import BaseModel
from interface_adapters.base_classes.response import ResponseBase
from sanic_openapi import doc


class DataStructure:

    maxTranslateTextPerDay: doc.Integer(
        description='Max translate text per day',
        required=True,
    )

    maxTranslateDcPerDay: doc.Integer(
        description='Max translate documents per day',
        required=True,
    )

    translationHistoryExpireDuration: doc.Integer(
        description='Translation history expire duration',
        required=True,
    )


class SystemSettingResponse(ResponseBase):

    data: DataStructure
