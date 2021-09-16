from infrastructure.configs.language import LanguageEnum
from typing import Optional, Union
from pydantic.fields import Field
from pydantic.main import BaseModel
from core.types import ExtendedEnum

TRANSLATION_REQUEST_EXPIRATION_TIME = 60 * 60
TASK_RESULT_FOLDER = 'task_result'
TASK_RESULT_FILE_PATTERN = '{}__{}.{}'
TASK_RESULT_FILE_EXTENSION = 'json'

def gen_task_result_file_path(created_at, task_id, file_extension):

    return TASK_RESULT_FILE_PATTERN.format(
        created_at, 
        task_id,
        file_extension
    )

class TaskTypeEnum(str, ExtendedEnum):

    file_translation = 'file_translation'
    plain_text_translation = 'plain_text_translation'
    language_detection = 'language_detection'

    public_file_translation = 'public_file_translation'
    public_plain_text_translation = 'public_plain_text_translation'
    public_language_detection = 'public_language_detection'

TRANSLATION_PUBLIC_TASKS = [
    TaskTypeEnum.public_file_translation.value,
    TaskTypeEnum.public_language_detection.value,
    TaskTypeEnum.public_plain_text_translation.value
]

TRANSLATION_PRIVATE_TASKS = [
    TaskTypeEnum.file_translation.value,
    TaskTypeEnum.language_detection.value,
    TaskTypeEnum.plain_text_translation.value
]

class CreatorTypeEnum(str, ExtendedEnum):

    end_user = 'end_user'

class StepStatusEnum(str, ExtendedEnum):

    not_yet_processed = 'not_yet_processed'
    in_progress = 'in_progress'
    completed = 'completed'
    cancelled = 'cancelled'

class TranslationStepEnum(str, ExtendedEnum):

    detecting_language = 'detecting_language'
    translating_language = 'translating_language'

class DetectionLanguageStepEnum(str, ExtendedEnum):

    detecting_language = 'detecting_language'

class LanguageNotYetDetectedResultFileSchemaV1(BaseModel):

    source_text: str 
    source_lang: Union[LanguageEnum, None] = Field(None, allow_mutation=False)

    target_text: Union[str, None] = Field(None, allow_mutation=False)
    target_lang: LanguageEnum 

    status: str = Field('language_not_yet_detected', allow_mutation=False) 

    schema_version: int = Field(1, allow_mutation=False) 

    class Config:
        use_enum_values = True
        validate_assignment = True

class NotYetTranslatedResultFileSchemaV1(BaseModel):

    source_text: str
    source_lang: LanguageEnum 

    target_text: Union[str, None] = Field(None, allow_mutation=False)
    target_lang: LanguageEnum 

    status: str = Field('not_yet_translated', allow_mutation=False) 

    schema_version: int = Field(1, allow_mutation=False) 

    class Config:
        use_enum_values = True
        validate_assignment = True

class TranslationCompletedResultFileSchemaV1(BaseModel):

    source_text: str
    source_lang: LanguageEnum

    target_text: str
    target_lang: LanguageEnum

    status: str = Field('translated', allow_mutation=False) 

    schema_version: int = Field(1, allow_mutation=False)  

    class Config:
        use_enum_values = True
        validate_assignment = True
