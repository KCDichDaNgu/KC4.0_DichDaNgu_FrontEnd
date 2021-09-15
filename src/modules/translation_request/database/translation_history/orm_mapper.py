from core.value_objects import ID, DateVO
from typing import Any
from infrastructure.database.base_classes.mongodb.orm_mapper_base import OrmMapperBase

from modules.translation_request.database.translation_history.orm_entity import TranslationHistoryOrmEntity
from modules.translation_request.domain.entities.translation_history import TranslationHistoryEntity, TranslationHistoryProps

class TranslationHistoryOrmMapper(OrmMapperBase[TranslationHistoryEntity, TranslationHistoryOrmEntity]):

    def __init__(self) -> None:
        super().__init__(entity_klass=TranslationHistoryEntity)

    def to_orm_entity(self, entity: TranslationHistoryEntity) -> TranslationHistoryOrmEntity:
        
        props = entity.get_props_copy()
        
        orm_props = {
            'creator_id': props.creator_id.value,
            'task_id': props.task_id.value,
            'translation_type': props.translation_type,
            'status': props.status,
            'file_path': props.file_path
        }
        
        return TranslationHistoryOrmEntity(**orm_props)

    def to_domain_props(self, orm_entity: TranslationHistoryOrmEntity) -> TranslationHistoryProps:

        props = {
            'creator_id': ID(str(orm_entity.creator_id)),
            'task_id': ID(str(orm_entity.task_id)),
            'translation_type': orm_entity.translation_type,
            'status': orm_entity.status,
            'file_path': orm_entity.file_path
        }

        return props
