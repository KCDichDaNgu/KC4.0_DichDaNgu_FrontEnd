from pydantic import BaseModel
from infrastructure.configs.language import LanguageEnum

class CreatePlainTextTranslationRequest(BaseModel):

    sourceText: str
    sourceLang: LanguageEnum
    translatedLang: LanguageEnum

    class Config:

        use_values_enum = True
