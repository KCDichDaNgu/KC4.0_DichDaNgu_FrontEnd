from pydantic import BaseModel
from typing import IO, Union

class CreateFileTranslationRequestCommand(BaseModel):
    
    source_file: IO
    source_lang: Union[str, None]
    target_lang: str
