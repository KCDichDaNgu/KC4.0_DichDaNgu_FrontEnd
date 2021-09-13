from pydantic import BaseModel

class CreatePlainTextTranslationRequestCommand(BaseModel):

    source_text: str
    source_lang: str
    target_lang: str
