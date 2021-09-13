import cassandra
from infrastructure.configs.main import GlobalConfig, get_cnf
from typing import List
from uuid import uuid4
from datetime import datetime
from cassandra.cqlengine.models import Model
from cassandra.cqlengine import columns
from cassandra.cqlengine.management import sync_table

from infrastructure.database.base_classes.aiocqlengine.model import AioModel

config: GlobalConfig = get_cnf()
database_config = config.CASSANDRA_DATABASE

class OrmEntityBase(AioModel):
    
    id = columns.UUID(primary_key=True, default=uuid4)
    created_at = columns.DateTime(required=True, default=datetime.now)
    updated_at = columns.DateTime(required=True, default=datetime.now)
    
    @classmethod
    def sync_table_to_db(
        cls, 
        keyspaces: List[str] = []
    ):

        __keyspaces = keyspaces if keyspaces else [database_config.KEYSPACE.NAME]

        sync_table(cls, keyspaces=__keyspaces)

    @classmethod
    def get_table_name(cls):
        return cls.__table_name__

    def to_dict(self):
        """ Returns a map of column names to cleaned values """
        values = self._dynamic_columns or {}

        for name, col in self._columns.items():
            values[name] = getattr(self, name, None)

        return values