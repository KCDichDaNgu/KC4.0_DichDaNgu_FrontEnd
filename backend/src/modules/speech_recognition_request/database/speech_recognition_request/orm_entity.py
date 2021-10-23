from umongo import fields, validate
from abc import ABC

from umongo import fields, validate

from infrastructure.configs import (
    get_mongodb_instance,
    MongoDBDatabase,
    GlobalConfig,
    get_cnf,
)
from modules.task.database.task.orm_entity import TaskOrmEntity
from infrastructure.configs.task import SpeechRecognitionTaskNameEnum

config: GlobalConfig = get_cnf()
database_config: MongoDBDatabase = config.MONGODB_DATABASE
db_instance = get_mongodb_instance()

@db_instance.register
class SpeechRecognitionRequestOrmEntity(TaskOrmEntity):

    task_name = fields.StringField(
        required=True,
        validate=validate.OneOf(SpeechRecognitionTaskNameEnum.enum_values()),
    )

    def pre_insert(self):

        super(SpeechRecognitionRequestOrmEntity, self).pre_insert()

        if self.task_name == SpeechRecognitionTaskNameEnum.private_speech_recognition and not self.creator_id:

            raise Exception("Creator cannot be None")
