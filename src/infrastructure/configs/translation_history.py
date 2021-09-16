from core.types import ExtendedEnum

class TranslationHistoryTypeEnum(str, ExtendedEnum):

    file_translation = 'file_translation'
    plain_text_translation = 'plain_text_translation'

    public_file_translation = 'public_file_translation'
    public_plain_text_translation = 'public_plain_text_translation'

TRANSLATION_HISTORY_PUBLIC_TYPES = [
    TranslationHistoryTypeEnum.public_file_translation.value,
    TranslationHistoryTypeEnum.public_plain_text_translation.value
]

TRANSLATION_HISTORY_PRIVATE_TYPES = [
    TranslationHistoryTypeEnum.file_translation.value,
    TranslationHistoryTypeEnum.plain_text_translation.value
]

class TranslationHistoryStatus(str, ExtendedEnum):

    translating = 'translating'
    translated = 'translated'

    cancelled = 'cancelled'
