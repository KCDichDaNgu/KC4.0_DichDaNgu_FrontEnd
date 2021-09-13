import cassandra
from infrastructure.configs.main import GlobalConfig, get_cnf
from typing import List
from uuid import uuid4
from datetime import datetime
from cassandra.cqlengine import columns
from cassandra.cqlengine.management import sync_table

from cassandra.cqlengine.query import BatchQuery

from infrastructure.database.base_classes.aiocqlengine.model import AioModel

config: GlobalConfig = get_cnf()
database_config = config.CASSANDRA_DATABASE

class OrmEntityBase(AioModel):
    
    id = columns.UUID(primary_key=True, default=uuid4)
    created_at = columns.DateTime(required=True, default=datetime.now)
    updated_at = columns.DateTime(required=True, default=datetime.now)

    # Before method
    @staticmethod
    def before_save(batch, *args, **kwargs):
        pass
    
    @staticmethod
    def before_create(batch, *args, **kwargs):
        pass

    @staticmethod
    def before_update(batch, *args, **kwargs):
        pass

    @staticmethod
    def before_delete(batch, *args, **kwargs):
        pass

    # After method
    @staticmethod
    def after_save(batch, *args, **kwargs):
        pass
    
    @staticmethod
    def after_create(batch, *args, **kwargs):
        pass

    @staticmethod
    def after_update(batch, *args, **kwargs):
        pass

    @staticmethod
    def after_delete(batch, *args, **kwargs):
        pass

    # Before async method
    @staticmethod
    async def async_before_save(batch, *args, **kwargs):
        pass
    
    @staticmethod
    async def async_before_create(batch, *args, **kwargs):
        pass

    @staticmethod
    async def async_before_update(batch, *args, **kwargs):
        pass

    @staticmethod
    async def async_before_delete(batch, *args, **kwargs):
        pass

    # After async method
    @staticmethod
    async def async_after_save(batch, *args, **kwargs):
        pass
    
    @staticmethod
    async def async_after_create(batch, *args, **kwargs):
        pass

    @staticmethod
    async def async_after_update(batch, *args, **kwargs):
        pass

    @staticmethod
    async def async_after_delete(batch, *args, **kwargs):
        pass

    @classmethod
    async def async_create_with_trigger(cls, **kwargs):

        with BatchQuery() as b:

            await cls.async_before_create(batch=b, **kwargs)

            result = await cls.batch(b).async_create(**kwargs)  

            await cls.async_after_create(batch=b, **kwargs)

            return result

    async def async_update_with_trigger(self, **values):

        with BatchQuery() as b:

            await self.__class__.async_before_update(batch=b, **values)

            result = await self.batch(b).async_update(**values)

            await self.async_after_update(batch=b, **values)

            return result

    async def async_save_with_trigger(self):

        with BatchQuery() as b:

            await self.__class__.async_before_save(batch=b)

            result = await self.batch(b).async_save()

            await self.async_after_save(batch=b)

            return result

    async def async_delete_with_trigger(self):

        with BatchQuery() as b:

            await self.__class__.async_before_delete(batch=b)

            result = await self.batch(b).async_delete()

            await self.async_after_delete(batch=b)

            return result

    @classmethod
    def create_with_trigger(cls, **kwargs):

        with BatchQuery() as b:

            cls.before_create(batch=b, **kwargs)

            result = cls.batch(b).create(**kwargs)

            cls.after_create(batch=b, **kwargs)

            return result

    def update_with_trigger(self, **values):

        with BatchQuery() as b:

            self.__class__.before_update(batch=b, **values)

            result = self.batch(b).update(**values)

            self.after_update(batch=b, **values)

            return result

    def save_with_trigger(self):

        with BatchQuery() as b:

            self.__class__.before_save(batch=b)

            result = self.batch(b).save()

            self.after_save(batch=b)

            return result

    def delete_with_trigger(self):

        with BatchQuery() as b:

            self.__class__.before_delete(batch=b)

            result = self.batch(b).delete()

            self.after_delete(batch=b)

            return result
    
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
        