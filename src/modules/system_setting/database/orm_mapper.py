from modules.system_setting.database.orm_entity import SystemSettingOrmEntity
from modules.system_setting.domain.entities.system_setting import SystemSettingEntity, SystemSettingProps
from core.value_objects.id import ID
from typing import Any
from infrastructure.database.base_classes.mongodb.orm_mapper_base import OrmMapperBase


class SystemSettingOrmMapper(OrmMapperBase[SystemSettingEntity, SystemSettingOrmEntity]):

    def __init__(self) -> None:
        super().__init__(entity_klass=SystemSettingEntity)

    def to_orm_entity(self, entity: SystemSettingEntity) -> SystemSettingOrmEntity:
        props = entity.get_props_copy()

        orm_props = {
            'editor_id': props.editor_id,
            'max_translate_doc_per_day': props.max_translate_doc_per_day,
            'max_translate_text_per_day': props.max_translate_text_per_day,
            'translation_history_expire_duration': props.translation_history_expire_duration,
        }

        return SystemSettingOrmEntity(**orm_props)

    def to_domain_props(self, orm_entity: SystemSettingOrmEntity) -> SystemSettingProps:

        props = {
            'editor_id':  orm_entity.editor_id,
            'max_translate_doc_per_day': orm_entity.max_translate_doc_per_day,
            'max_translate_text_per_day': orm_entity.max_translate_text_per_day,
            'translation_history_expire_duration': orm_entity.translation_history_expire_duration,
        }

        return props
