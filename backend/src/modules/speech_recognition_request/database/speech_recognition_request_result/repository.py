from modules.speech_recognition_request.database.speech_recognition_request_result.orm_mapper import SpeechRecognitionRequestResultOrmMapper
from modules.speech_recognition_request.database.speech_recognition_request_result.orm_entity import SpeechRecognitionRequestResultOrmEntity
from core.ports.repository import RepositoryPort
from modules.speech_recognition_request.domain.entities.speech_recognition_request_result import SpeechRecognitionRequestResultEntity, SpeechRecognitionRequestResultProps
from infrastructure.database.base_classes.mongodb.orm_repository_base import OrmRepositoryBase


from modules.task.database.task_result.repository import TasktResultRepositoryPort, TasktResultRepository

from typing import get_args

class SpeechRecognitionRequestResultRepositoryPort(
    TasktResultRepositoryPort,
    RepositoryPort[
        SpeechRecognitionRequestResultEntity, 
        SpeechRecognitionRequestResultProps
    ]
):

    pass

class SpeechRecognitionRequestResultRepository(
    TasktResultRepository,
    OrmRepositoryBase[
        SpeechRecognitionRequestResultEntity, 
        SpeechRecognitionRequestResultProps, 
        SpeechRecognitionRequestResultOrmEntity,
        SpeechRecognitionRequestResultOrmMapper
    ], 
    SpeechRecognitionRequestResultRepositoryPort
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
