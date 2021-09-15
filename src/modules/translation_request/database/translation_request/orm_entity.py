from datetime import timedelta
from core.value_objects.id import ID
from infrastructure.configs.main import MongoDBDatabase, GlobalConfig, get_cnf
from infrastructure.database.base_classes.mongodb import OrmEntityBase
from infrastructure.configs.translation_request import (
    TRANSLATION_PRIVATE_TASKS, EXPIRED_DURATION, CreatorTypeEnum, StepStatusEnum, TaskTypeEnum
)

from infrastructure.configs.main import get_mongodb_instance
from umongo import fields, validate

config: GlobalConfig = get_cnf()
database_config: MongoDBDatabase = config.MONGODB_DATABASE
db_instance = get_mongodb_instance()

@db_instance.register
class TranslationRequestOrmEntity(OrmEntityBase):

    creator_id = fields.UUIDField(default=None)

    task_type = fields.StrField(
        required=True, 
        validate=validate.OneOf([TaskTypeEnum.enum_values()])
    )

    creator_type = fields.StringField(
        required=True, 
        validate=validate.OneOf([CreatorTypeEnum.enum_values()])
    )

    status = fields.StringField(
        required=True,
        validate=validate.OneOf([StepStatusEnum.enum_values()])
    )

    current_step = fields.StringField(required=True, primary_key=True)
    expired_date = fields.DateTimeField(required=True)

    class Meta:
        collection_name = database_config.COLLECTIONS['translation_request']['name']

    
    def pre_insert(self):

        if self.created_at is not None and self.expired_date is None:

            self.expired_date = self.created_at + timedelta(seconds=EXPIRED_DURATION)

        if self.task_type in TRANSLATION_PRIVATE_TASKS and not self.creator_id:

            raise Exception('Creator cannot be None')
