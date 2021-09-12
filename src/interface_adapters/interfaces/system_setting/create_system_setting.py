from pydantic import BaseModel
from sanic_openapi.openapi2.doc import Integer

class CreateSystemSetting():

    maxTranslateTextPerDay: Integer
    maxTranslateDocPerDay: Integer
    translationHistoryExpireDuration: Integer
