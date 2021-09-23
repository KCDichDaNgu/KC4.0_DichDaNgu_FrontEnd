from interface_adapters.base_classes.response import ResponseBase
from sanic_openapi import doc

class DataStructure:

    maxUserTextTranslationPerDay: doc.Integer(
        description='Max user text translate per day',
        required=True,
    )

    maxUserDocTranslationPerDay: doc.Integer(
        description='Max user doc translate per day',
        required=True,
    )

    taskExpiredDuration: doc.Integer(
        description='Task expire duration',
        required=True,
    )

class SystemSettingResponse(ResponseBase):

    data: DataStructure
