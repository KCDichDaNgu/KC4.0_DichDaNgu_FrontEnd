from infrastructure.configs.database import MongoDBDatabase
from infrastructure.configs.main import CassandraDatabase, GlobalConfig, get_cnf
from infrastructure.database.base_classes.mongodb import OrmEntityBase
from cassandra.cqlengine import columns

config: GlobalConfig = get_cnf()
database_config: MongoDBDatabase = config.MONGODB_DATABASE


class SystemSettingOrmEntity(OrmEntityBase):

    __table_name__ = database_config.COLLECTIONS['system_setting']['name']

    editor_id = columns.UUID(default=None)
    max_translate_text_per_day = columns.Integer(required=True)
    max_translate_doc_per_day = columns.Integer(required=True)
    translation_history_expire_duration = columns.Integer(required=True)

    def validate(self):
        super(SystemSettingOrmEntity, self).validate()


# SystemSettingOrmEntity.sync_table_to_db()
