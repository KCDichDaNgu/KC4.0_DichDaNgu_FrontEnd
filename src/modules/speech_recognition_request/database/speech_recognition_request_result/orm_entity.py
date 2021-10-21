from umongo import fields, validate
from abc import ABC

from umongo import fields, validate

from infrastructure.configs import (
    get_mongodb_instance,
    MongoDBDatabase,
    GlobalConfig,
    get_cnf,
)
from infrastructure.configs.database import validate_orm_class_name
from modules.task.database.task_result.orm_entity import TaskResultOrmEntity

config: GlobalConfig = get_cnf()
database_config: MongoDBDatabase = config.MONGODB_DATABASE
db_instance = get_mongodb_instance()

@db_instance.register
@validate_orm_class_name
class SpeechRecognitionRequestResultOrmEntity(TaskResultOrmEntity):
    def pre_insert(self):

        super(SpeechRecognitionRequestResultOrmEntity, self).pre_insert()

    def pre_update(self):

        super(SpeechRecognitionRequestResultOrmEntity, self).pre_insert()
