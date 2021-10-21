from typing import get_args
from core.value_objects.id import ID
from infrastructure.database.base_classes.mongodb.orm_mapper_base import OrmMapperBase
from modules.speech_recognition_request.database.speech_recognition_history.orm_entity import \
    SpeechRecognitionHistoryOrmEntity
from modules.speech_recognition_request.domain.entities.speech_recognition_history import SpeechRecognitionHistoryEntity


class SpeechRecognitionHistoryOrmMapper(OrmMapperBase[SpeechRecognitionHistoryEntity, SpeechRecognitionHistoryOrmEntity]):

    @property
    def entity_klass(self):
        return get_args(self.__orig_bases__[0])[0]

    @property
    def orm_entity_klass(self):
        return get_args(self.__orig_bases__[0])[1]

    def to_orm_props(self, entity: SpeechRecognitionHistoryEntity):
            
        props = entity.get_props_copy()
        
        orm_props = {
            'creator_id': props.creator_id.value,
            'task_id': props.task_id.value,
            'speech_recognition_type': props.speech_recognition_type,
            'status': props.status,
            'file_path': props.file_path
        }
        
        return orm_props

    def to_domain_props(self, orm_entity: SpeechRecognitionHistoryOrmEntity):

        props = {
            'creator_id': ID(str(orm_entity.creator_id)),
            'task_id': ID(str(orm_entity.task_id)),
            'speech_recognition_type': orm_entity.speech_recognition_type,
            'status': orm_entity.status,
            'file_path': orm_entity.file_path,
        }

        return props