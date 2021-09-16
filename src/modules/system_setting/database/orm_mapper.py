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
            'uuid': props.id.value,
            'editor_id': props.editor_id,
            'max_translate_doc_per_day': props.max_translate_doc_per_day,
            'max_translate_text_per_day': props.max_translate_text_per_day,
            'translation_history_expire_duration': props.translation_history_expire_duration,
        }

        return orm_props

    def to_domain_props(self, orm_entity: SystemSettingOrmEntity):

        props = {
            'editor_id':  ID(str(orm_entity.editor_id)),
            'max_translate_doc_per_day': orm_entity.max_translate_doc_per_day,
            'max_translate_text_per_day': orm_entity.max_translate_text_per_day,
            'translation_history_expire_duration': orm_entity.translation_history_expire_duration,
        }

        return props
