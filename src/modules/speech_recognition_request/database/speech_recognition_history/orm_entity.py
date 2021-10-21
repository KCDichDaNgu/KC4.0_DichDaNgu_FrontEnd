from umongo import fields, validate

from infrastructure.configs import (
    get_mongodb_instance,
    MongoDBDatabase,
    GlobalConfig,
    get_cnf,
)
from infrastructure.configs.speech_recognition_history import (
    SpeechRecognitionHistoryTypeEnum,
    SpeechRecognitionHistoryStatus,
)

from infrastructure.database.base_classes.mongodb import OrmEntityBase

config: GlobalConfig = get_cnf()
database_config: MongoDBDatabase = config.MONGODB_DATABASE
db_instance = get_mongodb_instance()

@db_instance.register
class SpeechRecognitionHistoryOrmEntity(OrmEntityBase):

    creator_id = fields.UUIDField(default=None)
    task_id = fields.UUIDField(required=True)

    speech_recognition_type = fields.StringField(
        required=True,
        validate=validate.OneOf(SpeechRecognitionHistoryTypeEnum.enum_values()),
    )

    status = fields.StringField(
        required=True,
        validate=validate.OneOf(SpeechRecognitionHistoryStatus.enum_values()),
    )

    file_path = fields.StringField(allow_none=True)
    
    class Meta:
        collection_name = database_config.COLLECTIONS["speech_recognition_history"]["name"]

    def pre_insert(self):

        super(SpeechRecognitionHistoryOrmEntity, self).pre_insert()

        if self.file_path is None:
            raise Exception("File path cannot be None")

    def pre_update(self):

        super(SpeechRecognitionHistoryOrmEntity, self).pre_update()

        if self.file_path is None:
            raise Exception("File path cannot be None")
