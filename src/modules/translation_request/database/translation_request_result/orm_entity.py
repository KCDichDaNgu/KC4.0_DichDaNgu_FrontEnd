from infrastructure.configs.translation_request import TranslationStepEnum
from infrastructure.database.base_classes import OrmEntityBase
from cassandra.cqlengine import columns, ValidationError
from infrastructure.configs.main import CassandraDatabase, GlobalConfig, get_cnf

config: GlobalConfig = get_cnf()
database_config: CassandraDatabase = config.CASSANDRA_DATABASE

class TranslationRequestResultOrmEntity(OrmEntityBase):

    __table_name__ = database_config.TABLES['translation_request_result']['name']

    task_id = columns.UUID(required=True)
    step = columns.Text()
    file_path = columns.Text()

    def validate(self):
        
        super(TranslationRequestResultOrmEntity, self).validate()
        
        if not self.task_id or not self.step:

            raise ValidationError('Task id and step are invalid')

        if not self.step in TranslationStepEnum.enum_values():

            raise ValidationError('Step is invalid')

TranslationRequestResultOrmEntity.sync_table_to_db([database_config.KEYSPACE.NAME])
