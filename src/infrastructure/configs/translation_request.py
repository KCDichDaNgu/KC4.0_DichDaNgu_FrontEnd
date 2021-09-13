from core.types import ExtendedEnum

class TaskTypeEnum(str, ExtendedEnum):

    file_translation = 'file_translation'
    plain_text_translation = 'plain_text_translation'
    language_detection = 'language_detection'

    public_file_translation = 'public_file_translation'
    public_plain_text_translation = 'public_plain_text_translation'
    public_language_detection = 'public_language_detection'

public_tasks = [
    TaskTypeEnum.public_file_translation.value,
    TaskTypeEnum.public_language_detection.value,
    TaskTypeEnum.public_plain_text_translation.value
]

private_tasks = [
    TaskTypeEnum.file_translation.value,
    TaskTypeEnum.language_detection.value,
    TaskTypeEnum.plain_text_translation.value
]

class CreatorTypeEnum(str, ExtendedEnum):

    end_user = 'end_user'

class StatusEnum(str, ExtendedEnum):

    not_yet_processed = 'not_yet_processed'
    in_progress = 'in_progress'
    completed = 'completed'
    cancelled = 'cancelled'

class TranslationStepEnum(str, ExtendedEnum):

    detecting_language = 'detecting_language'
    translating_language = 'translating_language'

class DetectionLanguageStepEnum(str, ExtendedEnum):

    detecting_language = 'detecting_language'
