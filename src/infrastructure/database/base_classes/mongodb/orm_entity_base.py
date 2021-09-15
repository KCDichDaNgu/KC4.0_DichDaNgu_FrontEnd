from infrastructure.configs.main import get_mongodb_instance
from typing import List
from uuid import uuid4
from datetime import datetime

from umongo import Document, fields

db_instance = get_mongodb_instance()

@db_instance.register
class OrmEntityBase(Document):
    
    id = fields.UUIDField(unique=True, required=True)
    created_at = fields.DateTimeField(required=True)
    updated_at = fields.DateTimeField(required=True)

    def pre_insert(self):

        self.created_at = datetime.now()

    def pre_update(self):

        self.updated_at = datetime.now()

    class Meta:
        abstract = True
        indexes = ['-created_at']

    @classmethod
    def get_table_name(cls):
        return cls.collection
