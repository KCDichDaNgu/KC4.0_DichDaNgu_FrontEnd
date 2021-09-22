from interface_adapters.base_classes.response import ResponseBase
from sanic_openapi import doc

class DataStructure:

    maxUserTextTranslationPerDay = doc.Integer(
        description='Max user text translate per day'
    )

    maxUserDocTranslationPerDay = doc.Integer(
        description='Max user doc translate per day'
    )

    taskExpiredDuration = doc.Integer(
        description='Task expire duration'
    )

class SystemSettingResponse(ResponseBase):

    data: DataStructure
