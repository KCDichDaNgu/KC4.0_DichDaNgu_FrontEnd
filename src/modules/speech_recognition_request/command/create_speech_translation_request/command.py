from pydantic import BaseModel
from typing import Union
from sanic.request import File

from core.value_objects.id import ID

class CreateSpeechTranslationRequestCommand(BaseModel):

    creator_id: Union[ID, None]
    source_file: File
    source_lang: str
    target_lang: str
    
    class Config:
        arbitrary_types_allowed = True
