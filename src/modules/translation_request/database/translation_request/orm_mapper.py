from core.value_objects import ID, DateVO
from typing import Any
from infrastructure.database.base_classes.mongodb.orm_mapper_base import OrmMapperBase

from modules.translation_request.database.translation_request.orm_entity import TranslationRequestOrmEntity
from modules.translation_request.domain.entities.translation_request import TranslationRequestEntity, TranslationRequestProps

class TranslationRequestOrmMapper(OrmMapperBase[TranslationRequestEntity, TranslationRequestOrmEntity]):

    def __init__(self) -> None:
        super().__init__(entity_klass=TranslationRequestEntity)

    def to_orm_entity(self, entity: TranslationRequestEntity) -> TranslationRequestOrmEntity:
        
        props = entity.get_props_copy()
        
        orm_props = {
            'id': props.id.value,
            'created_at': props.created_at.value,
            'updated_at': props.updated_at.value,
            'creator_id': props.creator_id.value,
            'task_type': props.task_type,
            'creator_type': props.creator_type,
            'step_status': props.step_status,
            'current_step': props.current_step,
            'expired_date': props.expired_date.value,
        }
        
        return TranslationRequestOrmEntity(**orm_props)

    def to_domain_props(self, orm_entity: TranslationRequestOrmEntity) -> TranslationRequestProps:
        
        props = {
            'creator_id': ID(str(orm_entity.creator_id)),
            'task_type': orm_entity.task_type,
            'creator_type': orm_entity.creator_type,
            'step_status': orm_entity.step_status,
            'current_step': orm_entity.current_step,
            'expired_date': DateVO(orm_entity.expired_date)
        }

        return props
