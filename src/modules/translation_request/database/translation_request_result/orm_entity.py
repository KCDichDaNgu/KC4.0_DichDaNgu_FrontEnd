from infrastructure.configs.translation_request import TranslationStepEnum
from infrastructure.database.base_classes.mongodb import OrmEntityBase
from infrastructure.configs.main import MongoDBDatabase, GlobalConfig, get_cnf, get_mongodb_instance

from umongo import validate, fields

config: GlobalConfig = get_cnf()
database_config: MongoDBDatabase = config.MONGODB_DATABASE

db_instance = get_mongodb_instance()

@db_instance.register
class TranslationRequestResultOrmEntity(OrmEntityBase):

    task_id = fields.UUIDField(required=True)

    step = fields.StringField(
        required=True, 
    )

    file_path = fields.StringField(allow_none=True)

    class Meta:
        collection_name = database_config.COLLECTIONS['translation_request_result']['name']

    def pre_insert(self):

        super(self.__class__, self).pre_insert()
        
        if self.file_path is None:

            raise Exception('File path cannot be None')

    def pre_update(self):

        super(self.__class__, self).pre_insert()
        
        if self.file_path is None:

            raise Exception('File path cannot be None')
