from pydantic import BaseModel
from infrastructure.configs.language import LanguageEnum

class CreateSpeechRecognitionRequest():

    sourceText: str
