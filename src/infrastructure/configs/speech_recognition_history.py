from core.types import ExtendedEnum


class SpeechRecognitionHistoryTypeEnum(str, ExtendedEnum):

    public_speech_recognition = 'public_speech_recognition'
    private_speech_recognition = 'private_speech_recognition'

class SpeechRecognitionHistoryStatus(str, ExtendedEnum):

    converting = 'converting'
    converted = 'converted'

    closed = 'closed'
    cancelled = 'cancelled'
