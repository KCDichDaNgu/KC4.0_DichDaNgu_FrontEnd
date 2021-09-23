from infrastructure.configs.main import MongoDBDatabase, GlobalConfig, get_cnf, get_mongodb_instance
from infrastructure.database.base_classes.mongodb import OrmEntityBase
from umongo import fields, validate

config: GlobalConfig = get_cnf()
database_config: MongoDBDatabase = config.MONGODB_DATABASE
db_instance = get_mongodb_instance()

@db_instance.register
class DenyTokenOrmEntity(OrmEntityBase):
    token = fields.StringField(required=True, unique=True)
    expired_date = fields.DateField(required=True)  

    class Meta:
        collection_name = database_config.COLLECTIONS['deny_token']['name']  
        