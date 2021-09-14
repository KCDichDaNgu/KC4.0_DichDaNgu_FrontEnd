from infrastructure.configs.translation_history import TranslationHistoryTypeEnum, TranslationHistoryStatus
from infrastructure.database.base_classes import OrmEntityBase
from cassandra.cqlengine import columns, ValidationError
from infrastructure.configs.main import CassandraDatabase, GlobalConfig, get_cnf

config: GlobalConfig = get_cnf()
database_config: CassandraDatabase = config.CASSANDRA_DATABASE

class TranslationHistoryOrmEntity(OrmEntityBase):

    __table_name__ = database_config.TABLES['translation_history']['name']

    creator_id = columns.UUID(default=None)
    task_id = columns.UUID(required=True)
    task_result_id = columns.UUID(required=True)
    translation_type = columns.Text(required=True)
    status = columns.Text(required=True)
    file_path = columns.Text(required=True)

    def validate(self):
        
        super(TranslationHistoryOrmEntity, self).validate()
        
        if not self.task_id or not self.task_result_id:

            raise ValidationError('Task id and Task result id are invalid')

        if not self.translation_type in TranslationHistoryTypeEnum.enum_values():

            raise ValidationError('Translation type is invalid')

        if not self.translation_type in TranslationHistoryTypeEnum.enum_values():

            raise ValidationError('Translation History status is invalid')
