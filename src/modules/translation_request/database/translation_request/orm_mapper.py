from src.core.value_objects.id import ID
from typing import Any
from infrastructure.database.base_classes.orm_mapper_base import OrmMapper

from modules.translation_request.database.translation_request.orm_entity import TranslationRequestOrmEntity
from modules.translation_request.domain.entities.translation_request import TranslationRequestEntity, TranslationRequestProps

class TranslationRequestOrmMapper(OrmMapper[TranslationRequestEntity, TranslationRequestOrmEntity]):

    def to_orm_props(self, entity: TranslationRequestEntity) -> Any:
        
        props = entity.get_props_copy()

        orm_props = {
            'creator_id': props.creator_id.value,
            'task_type': props.task_type,
            'creator_type': props.creator_type,
            'status': props.status,
            'current_step': props.current_step,
            'expired_date': props.expired_date,
        }

        return orm_props

    def to_domain_props(self, orm_entity: TranslationRequestOrmEntity) -> TranslationRequestProps:
        
        props = {
            'creator_id': ID(orm_entity.id),
            'task_type': orm_entity.task_type,
            'creator_type': orm_entity.creator_type,
            'status': orm_entity.status,
            'current_step': orm_entity.current_step,
            'expired_date': orm_entity.expired_date
        }

        return props
