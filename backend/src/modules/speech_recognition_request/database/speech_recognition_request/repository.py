from modules.speech_recognition_request.database.speech_recognition_request.orm_mapper import SpeechRecognitionRequestOrmMapper
from modules.speech_recognition_request.database.speech_recognition_request.orm_entity import SpeechRecognitionRequestOrmEntity
from core.ports.repository import RepositoryPort
from modules.speech_recognition_request.domain.entities.speech_recognition_request import SpeechRecognitionRequestEntity, SpeechRecognitionRequestProps
from infrastructure.database.base_classes.mongodb.orm_repository_base import OrmRepositoryBase

from modules.task.database.task.repository import TaskRepository, TaskRepositoryPort

from typing import get_args

class SpeechRecognitionRequestRepositoryPort(
    TaskRepositoryPort,
    RepositoryPort[
        SpeechRecognitionRequestEntity, 
        SpeechRecognitionRequestProps
    ]
):

    pass

class SpeechRecognitionRequestRepository(
    TaskRepository,
    OrmRepositoryBase[
        SpeechRecognitionRequestEntity, 
        SpeechRecognitionRequestProps, 
        SpeechRecognitionRequestOrmEntity,
        SpeechRecognitionRequestOrmMapper
    ], 
    SpeechRecognitionRequestRepositoryPort
):

    @property
    def entity_klass(self):
        return get_args(self.__orig_bases__[1])[0]

    @property
    def repository(self):
        return get_args(self.__orig_bases__[1])[2]

    @property
    def mapper(self):
        return get_args(self.__orig_bases__[1])[3]
