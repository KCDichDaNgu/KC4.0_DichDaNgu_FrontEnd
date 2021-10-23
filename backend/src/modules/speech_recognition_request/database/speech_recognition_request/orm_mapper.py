from typing import get_args
from core.value_objects.date import DateVO
from core.value_objects.id import ID
from infrastructure.database.base_classes.mongodb.orm_mapper_base import OrmMapperBase
from modules.task.database.task.orm_mapper import TaskOrmMapper
from modules.speech_recognition_request.domain.entities.speech_recognition_request import (
    SpeechRecognitionRequestEntity,
)
from modules.speech_recognition_request.database.speech_recognition_request.orm_entity import (
    SpeechRecognitionRequestOrmEntity,
)

class SpeechRecognitionRequestOrmMapper(
    TaskOrmMapper,
    OrmMapperBase[SpeechRecognitionRequestEntity, SpeechRecognitionRequestOrmEntity],
):
    @property
    def entity_klass(self):
        return get_args(self.__orig_bases__[1])[0]

    @property
    def orm_entity_klass(self):
        return get_args(self.__orig_bases__[1])[1]

    def to_orm_props(self, entity: SpeechRecognitionRequestEntity):

        props = entity.get_props_copy()

        orm_props = {
            "creator_id": props.creator_id.value,
            "task_name": props.task_name,
            "creator_type": props.creator_type,
            "step_status": props.step_status,
            "current_step": props.current_step,
            "expired_date": props.expired_date.value,
        }

        return orm_props

    def to_domain_props(self, orm_entity: SpeechRecognitionRequestOrmEntity):

        props = {
            "creator_id": ID(str(orm_entity.creator_id)),
            "task_name": orm_entity.task_name,
            "creator_type": orm_entity.creator_type,
            "step_status": orm_entity.step_status,
            "current_step": orm_entity.current_step,
            "expired_date": DateVO(orm_entity.expired_date),
        }

        return props
