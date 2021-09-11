from src.infrastructure.configs.main import CassandraDatabase, GlobalConfig, get_cnf
from infrastructure.database.base_classes import OrmEntityBase
from infrastructure.configs.translation_request import TaskType
from cassandra.cqlengine import columns
from uuid import uuid4

config: GlobalConfig = get_cnf()
database_config: CassandraDatabase = config.CASSANDRA_DATABASE

class TranslationRequestOrmEntity(OrmEntityBase):

    __table_name__ = database_config.TABLES['']

    creator_id: columns.UUID(primary_key=True, default=uuid4)
    task_type: columns.Text(required=True, discriminator_column=True)
    creator_type: columns.Text(required=True)
    status: columns.Text(required=True)
    current_step: columns.Text(required=True)
    expired_date: columns.DateTime(required=True)

    def validate(self):
        super(TranslationRequestOrmEntity, self).validate()

class TranslationPlainTextRequestOrmEntity(TranslationRequestOrmEntity):

    __discriminator_value__ = TaskType.plain_text_translation.value

class LanguageDetectionRequestOrmEntity(TranslationRequestOrmEntity):

    __discriminator_value__ = TaskType.language_detection.value
