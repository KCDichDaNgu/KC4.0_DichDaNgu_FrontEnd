from infrastructure.configs.main import CassandraDatabase, GlobalConfig, get_cnf
from infrastructure.database.base_classes import OrmEntityBase
from infrastructure.configs.translation_request import TaskTypeEnum, private_tasks
from cassandra.cqlengine import ValidationError, columns
from uuid import uuid4

config: GlobalConfig = get_cnf()
database_config: CassandraDatabase = config.CASSANDRA_DATABASE

class TranslationRequestOrmEntity(OrmEntityBase):

    __table_name__ = database_config.TABLES['translation_request']['name']

    creator_id = columns.UUID(default=None)
    task_type = columns.Text(required=True)
    creator_type = columns.Text(required=True)
    status = columns.Text(required=True)
    current_step = columns.Text(required=True)
    expired_date = columns.DateTime()

    def validate(self):
        
        super(TranslationRequestOrmEntity, self).validate()
        
        if self.task_type in private_tasks and not self.creator_id:

            raise ValidationError('Creator cannot be None')

TranslationRequestOrmEntity.sync_table_to_db()
