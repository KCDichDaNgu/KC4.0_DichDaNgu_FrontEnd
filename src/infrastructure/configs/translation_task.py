from infrastructure.configs.language import LanguageEnum
from typing import Optional, Union
from pydantic.fields import Field
from pydantic.main import BaseModel
from core.types import ExtendedEnum
from infrastructure.configs.message import MESSAGES

class TranslationTaskNameEnum(str, ExtendedEnum):

    private_file_translation = 'private_file_translation'
    private_plain_text_translation = 'private_plain_text_translation'

    public_file_translation = 'public_file_translation'
    public_plain_text_translation = 'public_plain_text_translation'

TRANSLATION_PUBLIC_TASKS = [
    TranslationTaskNameEnum.public_file_translation.value,
    TranslationTaskNameEnum.public_plain_text_translation.value
]

TRANSLATION_PRIVATE_TASKS = [
    TranslationTaskNameEnum.private_file_translation.value,
    TranslationTaskNameEnum.private_plain_text_translation.value
]

class TranslationTaskStepEnum(str, ExtendedEnum):
    
    detecting_language = 'detecting_language'
    translating_language = 'translating_language'

RESULT_FILE_STATUS = {
    'language_not_yet_detected': 'language_not_yet_detected',
    'not_yet_translated': 'not_yet_translated',
    'closed': 'closed',
    'translated': 'translated'
}
    
class TranslationTask_LangUnknownResultFileSchemaV1(BaseModel):

    source_text: str 
    source_lang: Union[LanguageEnum, None] = Field(None, allow_mutation=False)

    target_text: Union[str, None] = Field(None, allow_mutation=False)
    target_lang: LanguageEnum 

    task_name: TranslationTaskNameEnum

    status: str = Field(RESULT_FILE_STATUS['language_not_yet_detected'], allow_mutation=False) 
    message: str = ''

    schema_version: int = Field(1, allow_mutation=False) 

    class Config:
        use_enum_values = True
        validate_assignment = True

class TranslationTask_NotYetTranslatedResultFileSchemaV1(BaseModel):

    source_text: str
    source_lang: LanguageEnum 

    target_text: Union[str, None] = Field(None, allow_mutation=False)
    target_lang: LanguageEnum 

    task_name: TranslationTaskNameEnum

    status: str = Field(RESULT_FILE_STATUS['not_yet_translated'], allow_mutation=False) 
    message: str = ''

    schema_version: int = Field(1, allow_mutation=False) 

    class Config:
        use_enum_values = True
        validate_assignment = True


class TranslationTask_TranslationClosedResultFileSchemaV1(BaseModel):

    source_text: str
    source_lang: LanguageEnum

    target_text: Union[str, None] = Field(None, allow_mutation=False)
    target_lang: LanguageEnum

    task_name: TranslationTaskNameEnum

    status: str = Field(RESULT_FILE_STATUS['closed'], allow_mutation=False) 
    message: str = ''

    schema_version: int = Field(1, allow_mutation=False)  

    class Config:
        use_enum_values = True
        validate_assignment = True

class TranslationTask_TranslationCompletedResultFileSchemaV1(BaseModel):

    source_text: str
    source_lang: LanguageEnum

    target_text: str
    target_lang: LanguageEnum

    task_name: TranslationTaskNameEnum

    status: str = Field(RESULT_FILE_STATUS['translated'], allow_mutation=False) 
    message: str = ''

    schema_version: int = Field(1, allow_mutation=False)  

    class Config:
        use_enum_values = True
        validate_assignment = True

SOURCE_FILE_FOLDER = 'source_file'
TARGET_FILE_FOLDER = 'target_file'

def gen_source_file_file_path(task_id):

    return '{}_{}'.format('source_file', task_id)

def gen_target_file_file_path(task_id):

    return '{}_{}'.format('target_file', task_id)

class FileTranslationTask_LangUnknownResultFileSchemaV1(BaseModel):

    source_file_path: str 
    source_lang: Union[LanguageEnum, None] = Field(None, allow_mutation=False)

    target_file_path: Union[str, None] = Field(None, allow_mutation=False)
    target_lang: LanguageEnum 

    task_name: TranslationTaskNameEnum

    status: str = Field(RESULT_FILE_STATUS['language_not_yet_detected'], allow_mutation=False) 
    message: str = ''

    schema_version: int = Field(1, allow_mutation=False) 

    class Config:
        use_enum_values = True
        validate_assignment = True

class FileTranslationTask_NotYetTranslatedResultFileSchemaV1(BaseModel):

    source_file_path: str
    source_lang: LanguageEnum 

    target_file_path: Union[str, None] = Field(None, allow_mutation=False)
    target_lang: LanguageEnum 

    task_name: TranslationTaskNameEnum

    status: str = Field(RESULT_FILE_STATUS['not_yet_translated'], allow_mutation=False) 
    message: str = ''

    schema_version: int = Field(1, allow_mutation=False) 

    class Config:
        use_enum_values = True
        validate_assignment = True


class FileTranslationTask_TranslationClosedResultFileSchemaV1(BaseModel):

    source_file_path: str
    source_lang: LanguageEnum

    target_file_path: Union[str, None] = Field(None, allow_mutation=False)
    target_lang: LanguageEnum

    task_name: TranslationTaskNameEnum

    status: str = Field(RESULT_FILE_STATUS['closed'], allow_mutation=False) 
    message: str = ''

    schema_version: int = Field(1, allow_mutation=False)  

    class Config:
        use_enum_values = True
        validate_assignment = True

class FileTranslationTask_TranslationCompletedResultFileSchemaV1(BaseModel):

    source_file_path: str
    source_lang: LanguageEnum

    target_file_path: str
    target_lang: LanguageEnum

    task_name: TranslationTaskNameEnum

    status: str = Field(RESULT_FILE_STATUS['translated'], allow_mutation=False) 
    message: str = ''

    schema_version: int = Field(1, allow_mutation=False)  

    class Config:
        use_enum_values = True
        validate_assignment = True
