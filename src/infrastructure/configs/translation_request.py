from enum import Enum

class TaskType(str, Enum):

    file_translation = 'file_translation'
    plain_text_translation = 'plain_text_translation'
    language_detection = 'language_detection'

    public_file_translation = 'public_file_translation'
    public_plain_text_translation = 'public_plain_text_translation'
    public_language_detection = 'public_language_detection'

class CreatorType(str, Enum):

    end_user = 'end_user'

class Status(str, Enum):

    not_yet_processed = 'not_yet_processed'
    in_progress = 'in_progress'
    completed = 'completed'
    cancelled = 'cancelled'

class TranslationStep(str, Enum):

    detecting_language = 'detecting_language'
    translating_language = 'translating_language'

class DetectionLanguageStep(str, Enum):

    detecting_language = 'detecting_language'
