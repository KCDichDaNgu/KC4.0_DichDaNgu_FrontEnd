from core.types import ExtendedEnum

EXPIRED_DURATION = 60

TASK_RESULT_FOLDER = 'task_result'
TASK_RESULT_FILE_PATTERN = '{}__{}'
TASK_RESULT_FILE_EXTENSION = 'json'

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
