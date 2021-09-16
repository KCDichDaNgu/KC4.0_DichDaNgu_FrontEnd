from pydantic import BaseModel
from typing import Union

class CreatePlainTextTranslationRequestCommand(BaseModel):

    source_text: str
    source_lang: Union[str, None]
    target_lang: str
