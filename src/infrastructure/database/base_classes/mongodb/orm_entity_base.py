from infrastructure.configs.main import get_mongodb_instance
from typing import List
from uuid import uuid4
from datetime import datetime

from umongo import Document, fields, pre_load

db_instance = get_mongodb_instance()

@db_instance.register
class OrmEntityBase(Document):
    
    uuid = fields.UUIDField(unique=True, required=True)
    created_at = fields.DateTimeField(allow_none=True)
    updated_at = fields.DateTimeField(allow_none=True)
    class Meta:
        abstract = True
        indexes = ['-created_at']

    def pre_insert(self):
        
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    @classmethod
    def get_table_name(cls):
        return cls.collection
