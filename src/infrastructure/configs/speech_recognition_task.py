from pydantic.fields import Field
from pydantic.main import BaseModel
from core.utils.file import extract_file_extension
from infrastructure.configs.language import LanguageEnum
from core.types import ExtendedEnum

SPEECH_RECOGNITION_FOLDER_PATH = "speech_recognition"
SPEECH_RECOGNITION_SOURCE_FILE_NAME = "source_file"
SPEECH_RECOGNITION_TARGET_FILE_NAME = "target_file"

RESULT_FILE_STATUS = {
    "not_yet_converted": "not_yet_converted",
    "closed": "closed",
    "converted": "converted",
    "converting": "converting",
}

class AllowedSpeechRecognitionExtension(str, ExtendedEnum):

    mp3 = 'mp3'
    wav = 'wav'
    aac = 'aac'

def is_allowed_file_extension(file_name):

    file_ext = extract_file_extension(file_name)

    return file_ext in AllowedSpeechRecognitionExtension.enum_values()


def get_speech_recognition_file_path(task_id, file_name: str):

    return f"{SPEECH_RECOGNITION_FOLDER_PATH}/{task_id}/{file_name}"


def get_speech_recognition_source_file_name():

    return SPEECH_RECOGNITION_SOURCE_FILE_NAME

def get_speech_recognition_target_file_name():

    return SPEECH_RECOGNITION_TARGET_FILE_NAME




class SpeechRecognitionTaskNameEnum(str, ExtendedEnum):

    public_speech_recognition = "public_speech_recognition"
    private_speech_recognition = "private_speech_recognition"


class SpeechRecognitionTaskStepEnum(str, ExtendedEnum):

    converting_speech = "converting_speech"


class SpeechRecognitionTask_NotYetConvertedResultFileSchemaV1(BaseModel):
    source_file_full_path: str

    source_lang: LanguageEnum

    task_name: SpeechRecognitionTaskNameEnum

    status: str = Field(RESULT_FILE_STATUS["not_yet_converted"], allow_mutation=False)
    message: str = ""

    schema_version: int = Field(1, allow_mutation=False)

    class Config:
        use_enum_values = True
        validate_assignment = True

class SpeechRecognitionTask_ConvertingResultFileSchemaV1(BaseModel):
    source_file_full_path: str

    source_lang: LanguageEnum
    job_id: str

    task_name: SpeechRecognitionTaskNameEnum

    status: str = Field(RESULT_FILE_STATUS["converting"], allow_mutation=False)
    message: str = ""

    schema_version: int = Field(1, allow_mutation=False)

    class Config:
        use_enum_values = True
        validate_assignment = True

class SpeechRecognitionTask_ConvertedResultFileSchemaV1(BaseModel):
    source_file_full_path: str
    target_file_full_path: str
    job_id: str

    source_lang: LanguageEnum

    task_name: SpeechRecognitionTaskNameEnum

    status: str = Field(RESULT_FILE_STATUS["converted"], allow_mutation=False)
    message: str = ""

    schema_version: int = Field(1, allow_mutation=False)

    class Config:
        use_enum_values = True
        validate_assignment = True

class SpeechRecognitionTask_ClosedResultFileSchemaV1(BaseModel):
    source_file_full_path: str

    source_lang: LanguageEnum

    task_name: SpeechRecognitionTaskNameEnum

    status: str = Field(RESULT_FILE_STATUS["closed"], allow_mutation=False)
    message: str = ""

    schema_version: int = Field(1, allow_mutation=False)

    class Config:
        use_enum_values = True
        validate_assignment = True
