from infrastructure.configs.language import LanguageEnum
from typing import Optional, Union
from pydantic.fields import Field
from pydantic.main import BaseModel
from core.types import ExtendedEnum

class LanguageDetectionTaskNameEnum(str, ExtendedEnum):

    private_file_language_detection = 'private_file_language_detection'
    private_plain_text_language_detection = 'private_plain_text_language_detection'

    public_file_language_detection = 'public_file_language_detection'
    public_plain_text_language_detection = 'public_plain_text_language_detection'

LANGUAGE_DETECTION_PUBLIC_TASKS = [
    LanguageDetectionTaskNameEnum.public_file_language_detection.value,
    LanguageDetectionTaskNameEnum.public_plain_text_language_detection.value
]

LANGUAGE_DETECTION_PRIVATE_TASKS = [
    LanguageDetectionTaskNameEnum.private_file_language_detection.value,
    LanguageDetectionTaskNameEnum.private_plain_text_language_detection.value
]

class LanguageDetectionTaskStepEnum(str, ExtendedEnum):

    detecting_language = 'detecting_language'

class LanguageDetectionTask_LangUnknownResultFileSchemaV1(BaseModel):

    source_text: str 
    source_lang: Union[LanguageEnum, None] = Field(None, allow_mutation=False) 

    task_name: LanguageDetectionTaskNameEnum

    status: str = Field('language_not_yet_detected', allow_mutation=False) 

    schema_version: int = Field(1, allow_mutation=False) 

    class Config:
        use_enum_values = True
        validate_assignment = True

class LanguageDetectionTask_LanguageDetectionCompletedResultFileSchemaV1(BaseModel):

    source_text: str
    source_lang: LanguageEnum

    task_name: LanguageDetectionTaskNameEnum 
    
    status: str = Field('language_detected', allow_mutation=False) 

    schema_version: int = Field(1, allow_mutation=False)  

    class Config:
        use_enum_values = True
        validate_assignment = True
