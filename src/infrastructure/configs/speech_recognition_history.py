from core.types import ExtendedEnum

class SpeechRecognitionHistoryTypeEnum(str, ExtendedEnum):

    public_speech_recognition = "public_speech_recognition"
    private_speech_recognition = "private_speech_recognition"

    public_speech_translation = "public_speech_translation"
    private_speech_translation = "private_speech_translation"

class SpeechRecognitionHistoryStatus(str, ExtendedEnum):

    converting = "converting"
    converted = "converted"
    translated = "translated"
    translating = "translating"

    closed = "closed"
    cancelled = "cancelled"
