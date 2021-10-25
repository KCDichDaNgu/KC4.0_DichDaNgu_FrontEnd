
from core.ports.repository import RepositoryPort
from infrastructure.database.base_classes.mongodb.orm_repository_base import OrmRepositoryBase

from typing import get_args
from modules.speech_recognition_request.database.speech_recognition_history.orm_entity import SpeechRecognitionHistoryOrmEntity
from modules.speech_recognition_request.database.speech_recognition_history.orm_mapper import SpeechRecognitionHistoryOrmMapper
from modules.speech_recognition_request.domain.entities.speech_recognition_history import SpeechRecognitionHistoryEntity, SpeechRecognitionHistoryProps

class SpeechRecognitionHistoryRepositoryPort(RepositoryPort[SpeechRecognitionHistoryEntity, SpeechRecognitionHistoryProps]):

    pass

class SpeechRecognitionHistoryRepository(
    OrmRepositoryBase[
        SpeechRecognitionHistoryEntity, 
        SpeechRecognitionHistoryOrmMapper, 
        SpeechRecognitionHistoryOrmEntity,
        SpeechRecognitionHistoryOrmMapper
    ], 
    SpeechRecognitionHistoryRepositoryPort
):
    
    @property
    def entity_klass(self):
        return get_args(self.__orig_bases__[0])[0]

    @property
    def repository(self):
        return get_args(self.__orig_bases__[0])[2]

    @property
    def mapper(self):
        return get_args(self.__orig_bases__[0])[3]
