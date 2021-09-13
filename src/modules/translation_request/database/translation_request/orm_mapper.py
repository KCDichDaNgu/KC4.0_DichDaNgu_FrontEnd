from core.value_objects import ID, DateVO
from typing import Any
from infrastructure.database.base_classes.orm_mapper_base import OrmMapperBase

from modules.translation_request.database.translation_request.orm_entity import TranslationRequestOrmEntity
from modules.translation_request.domain.entities.translation_request import TranslationRequestEntity, TranslationRequestProps

class TranslationRequestOrmMapper(OrmMapperBase[TranslationRequestEntity, TranslationRequestOrmEntity]):

    def __init__(self) -> None:
        super().__init__(entity_klass=TranslationRequestEntity)

    def to_orm_entity(self, entity: TranslationRequestEntity) -> TranslationRequestOrmEntity:
        
        props = entity.get_props_copy()
        
        orm_props = {
            'creator_id': props.creator_id,
            'task_type': props.task_type,
            'creator_type': props.creator_type,
            'status': props.status,
            'current_step': props.current_step,
            'expired_date': props.expired_date,
        }
        
        return TranslationRequestOrmEntity(**orm_props)

    def to_domain_props(self, orm_entity: TranslationRequestOrmEntity) -> TranslationRequestProps:

        props = {
            'creator_id': orm_entity.id,
            'task_type': orm_entity.task_type,
            'creator_type': orm_entity.creator_type,
            'status': orm_entity.status,
            'current_step': orm_entity.current_step,
            'expired_date': orm_entity.expired_date
        }

        return props

    def assign_props_to_entity(
        self, 
        entity_props: Any,
        orm_entity: TranslationRequestOrmEntity
    ) -> TranslationRequestEntity:
    
        return TranslationRequestEntity.from_orm({
            **entity_props,
            "id": ID(str(orm_entity.id)),
            "created_at": DateVO(orm_entity.created_at),
            "updated_at": DateVO(orm_entity.updated_at),
            "expired_date": DateVO(orm_entity.expired_date) if orm_entity.expired_date else None
        })
