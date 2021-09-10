from core.base_classes.entity import Entity
from cassandra.cqlengine import columns


class SystemSettingEntity(Entity):
    
    editor_id: columns.ID
    max_translate_text_per_day: columns.Integer
    max_translate_doc_per_day:  columns.Integer
    translation_history_expire_duration: columns.DateVO

    class Meta:
        table_name = 'system_setting'
