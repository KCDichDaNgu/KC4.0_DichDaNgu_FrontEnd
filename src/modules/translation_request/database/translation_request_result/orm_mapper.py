from core.value_objects import ID, DateVO
from typing import Any
from infrastructure.database.base_classes.orm_mapper_base import OrmMapperBase

from modules.translation_request.database.translation_request_result.orm_entity import TranslationRequestResultOrmEntity
from modules.translation_request.domain.entities.translation_request_result import TranslationRequestResultEntity, TranslationRequestResultProps

class TranslationRequestResultOrmMapper(OrmMapperBase[TranslationRequestResultEntity, TranslationRequestResultOrmEntity]):

    def __init__(self) -> None:
        super().__init__(entity_klass=TranslationRequestResultEntity)

    def to_orm_entity(self, entity: TranslationRequestResultEntity) -> TranslationRequestResultOrmEntity:
        
        props = entity.get_props_copy()
        
        orm_props = {
            'task_id': props.task_id.value,
            'step': props.step,
            'file_path': props.file_path
        }
        
        return TranslationRequestResultOrmEntity(**orm_props)

    def to_domain_props(self, orm_entity: TranslationRequestResultOrmEntity) -> TranslationRequestResultProps:

        props = {
            'task_id': ID(str(orm_entity.task_id)),
            'step': orm_entity.step,
            'file_path': orm_entity.file_path
        }

        return props
