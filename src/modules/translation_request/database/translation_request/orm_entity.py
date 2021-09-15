from datetime import timedelta, datetime

from marshmallow.decorators import post_dump, post_load, pre_dump
from umongo.document import Document
from core.value_objects.id import ID
from infrastructure.configs.main import MongoDBDatabase, GlobalConfig, get_cnf
from infrastructure.database.base_classes.mongodb import OrmEntityBase
from infrastructure.configs.translation_request import (
    TRANSLATION_PRIVATE_TASKS, TRANSLATION_REQUEST_EXPIRATION_TIME, CreatorTypeEnum, StepStatusEnum, TaskTypeEnum
)

from infrastructure.configs.main import get_mongodb_instance
from umongo import fields, validate, pre_load

config: GlobalConfig = get_cnf()
database_config: MongoDBDatabase = config.MONGODB_DATABASE
db_instance = get_mongodb_instance()

@db_instance.register
class TranslationRequestOrmEntity(OrmEntityBase):

    creator_id = fields.UUIDField(allow_none=True)

    task_type = fields.StringField(
        required=True, 
        validate=validate.OneOf(TaskTypeEnum.enum_values())
    )

    creator_type = fields.StringField(
        required=True, 
        validate=validate.OneOf(CreatorTypeEnum.enum_values())
    )

    step_status = fields.StringField(
        required=True,
        validate=validate.OneOf(StepStatusEnum.enum_values())
    )

    current_step = fields.StringField(
        required=True
    )

    expired_date = fields.DateTimeField(required=True, allow_none=True)

    class Meta:
        collection_name = database_config.COLLECTIONS['translation_request']['name']

    
    def pre_insert(self):

        super(self.__class__, self).pre_insert()
        
        if self.created_at is not None and self.expired_date is None:

            self.expired_date = self.created_at + timedelta(seconds=TRANSLATION_REQUEST_EXPIRATION_TIME)

        if self.task_type in TRANSLATION_PRIVATE_TASKS and not self.creator_id:

            raise Exception('Creator cannot be None')
