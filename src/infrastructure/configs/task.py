from infrastructure.configs.language import LanguageEnum
from typing import Optional, Union
from pydantic.fields import Field
from pydantic.main import BaseModel
from core.types import ExtendedEnum

TASK_EXPIRATION_TIME = 60 * 60
TASK_RESULT_FOLDER = 'task_result'
TASK_RESULT_FILE_PATTERN = '{}__{}.{}'
TASK_RESULT_FILE_EXTENSION = 'json'

def gen_task_result_file_path(created_at, task_id, file_extension):

    return TASK_RESULT_FILE_PATTERN.format(
        created_at, 
        task_id,
        file_extension
    )

class TranslationTaskNameEnum(str, ExtendedEnum):

    private_file_translation = 'private_file_translation'
    private_plain_text_translation = 'private_plain_text_translation'

    public_file_translation = 'public_file_translation'
    public_plain_text_translation = 'public_plain_text_translation'
    

class LanguageDetectionTaskNameEnum(str, ExtendedEnum):

    public_plain_text_language_detection = 'public_plain_text_language_detection'
    public_file_language_detection = 'public_file_language_detection'

    private_plain_text_language_detection = 'private_plain_text_language_detection'
    private_file_language_detection = 'private_file_language_detection'

TRANSLATION_PUBLIC_TASKS = [
    TranslationTaskNameEnum.public_file_translation.value,
    TranslationTaskNameEnum.public_plain_text_translation.value
]

TRANSLATION_PRIVATE_TASKS = [
    TranslationTaskNameEnum.private_file_translation.value,
    TranslationTaskNameEnum.private_plain_text_translation.value
]

LANGUAGE_DETECTION_PUBLIC_TASKS = [
    LanguageDetectionTaskNameEnum.public_plain_text_language_detection.value,
    LanguageDetectionTaskNameEnum.public_file_language_detection.value
]

LANGUAGE_DETECTION_PRIVATE_TASKS = [
    LanguageDetectionTaskNameEnum.private_plain_text_language_detection.value,
    LanguageDetectionTaskNameEnum.private_file_language_detection.value
]

class TaskTypeEnum(str, ExtendedEnum):

    unclassified = 'unclassified'
    translation_task = 'translation_task'
    language_detection = 'language_detection'

class CreatorTypeEnum(str, ExtendedEnum):

    end_user = 'end_user'

class StepStatusEnum(str, ExtendedEnum):

    not_yet_processed = 'not_yet_processed'
    in_progress = 'in_progress' # Trong trường hợp task bị kéo dài, k rõ bao h xong 
    completed = 'completed'
    cancelled = 'cancelled'

class TranslationTaskStepEnum(str, ExtendedEnum):

    detecting_language = 'detecting_language'
    translating_language = 'translating_language'

class LanguageDetectionTaskStepEnum(str, ExtendedEnum):

    detecting_language = 'detecting_language'

class TranslationTask_LangUnknownResultFileSchemaV1(BaseModel):

    source_text: str 
    source_lang: Union[LanguageEnum, None] = Field(None, allow_mutation=False)

    target_text: Union[str, None] = Field(None, allow_mutation=False)
    target_lang: LanguageEnum 

    status: str = Field('language_not_yet_detected', allow_mutation=False) 

    schema_version: int = Field(1, allow_mutation=False) 

    class Config:
        use_enum_values = True
        validate_assignment = True

class TranslationTask_NotYetTranslatedResultFileSchemaV1(BaseModel):

    source_text: str
    source_lang: LanguageEnum 

    target_text: Union[str, None] = Field(None, allow_mutation=False)
    target_lang: LanguageEnum 

    status: str = Field('not_yet_translated', allow_mutation=False) 

    schema_version: int = Field(1, allow_mutation=False) 

    class Config:
        use_enum_values = True
        validate_assignment = True

class TranslationTask_TranslationCompletedResultFileSchemaV1(BaseModel):

    source_text: str
    source_lang: LanguageEnum

    target_text: str
    target_lang: LanguageEnum

    status: str = Field('translated', allow_mutation=False) 

    schema_version: int = Field(1, allow_mutation=False)  

    class Config:
        use_enum_values = True
        validate_assignment = True
