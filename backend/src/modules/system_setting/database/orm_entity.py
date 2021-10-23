from infrastructure.configs.main import MongoDBDatabase, GlobalConfig, get_cnf
from infrastructure.configs.main import get_mongodb_instance
from infrastructure.database.base_classes.mongodb import OrmEntityBase
from umongo import fields, validate

config: GlobalConfig = get_cnf()
database_config: MongoDBDatabase = config.MONGODB_DATABASE
db_instance = get_mongodb_instance()

@db_instance.register
class SystemSettingOrmEntity(OrmEntityBase):

    editor_id = fields.UUIDField(allow_none=True)
    max_user_text_translation_per_day = fields.IntegerField(required=True)
    max_user_doc_translation_per_day = fields.IntegerField(required=True)
    task_expired_duration = fields.IntegerField(required=True)
    
    class Meta:
        collection_name = database_config.COLLECTIONS['system_setting']['name']

    def pre_insert(self):
        super(SystemSettingOrmEntity, self).pre_insert()

    def pre_update(self):

        super(SystemSettingOrmEntity, self).pre_update()
