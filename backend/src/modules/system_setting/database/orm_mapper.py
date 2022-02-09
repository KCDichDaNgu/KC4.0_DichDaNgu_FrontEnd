from modules.system_setting.database.orm_entity import SystemSettingOrmEntity
from modules.system_setting.domain.entities.system_setting import SystemSettingEntity, SystemSettingProps
from core.value_objects.id import ID
from typing import Any, get_args
from infrastructure.database.base_classes.mongodb.orm_mapper_base import OrmMapperBase

class SystemSettingOrmMapper(OrmMapperBase[SystemSettingEntity, SystemSettingOrmEntity]):

    @property
    def entity_klass(self):
        return get_args(self.__orig_bases__[0])[0]

    @property
    def orm_entity_klass(self):
        return get_args(self.__orig_bases__[0])[1]

    def to_orm_props(self, entity: SystemSettingEntity):
        props = entity.get_props_copy()

        orm_props = {
            'editor_id': props.editor_id.value,
            'max_user_doc_translation_per_day': props.max_user_doc_translation_per_day,
            'max_user_text_translation_per_day': props.max_user_text_translation_per_day,
            'task_expired_duration': props.task_expired_duration,
        }

        return orm_props

    def to_domain_props(self, orm_entity: SystemSettingOrmEntity):
        props = {
            'editor_id':  ID(str(orm_entity.editor_id)),
            'max_user_doc_translation_per_day': orm_entity.max_user_doc_translation_per_day,
            'max_user_text_translation_per_day': orm_entity.max_user_text_translation_per_day,
            'task_expired_duration': orm_entity.task_expired_duration,
        }

        return props
