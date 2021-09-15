from typing import Any, Dict
from pydantic import BaseModel, Field
from umongo.frameworks import MotorAsyncIOInstance

class KeySpaceConfig(BaseModel):

    NAME: str = Field(None)

    DURABLE_WRITES: bool = True
    STRATEGY_CLASS: str = 'SimpleStrategy'
    STRATEGY_OPTIONS: dict = {'replication_factor': 1}
    CONNECTIONS: Any = None

class CassandraDatabase(BaseModel):
    
    NAME: str = Field(None)
    PASSWORD: str = Field(None)
    USER: str = Field(None)
    HOST: str = Field(None)

    SCHEMA_VERSION = 1

    KEYSPACE: KeySpaceConfig
    
    PROTOCOL_VERSION: int = 3

    TABLES: dict = {
        "translation_request": {
            "name": "translation_request"
        },
        "translation_request_result": {
            "name": "translation_request_result"
        },
        "translation_history": {
            "name": "translation_history"
        }
    }

class MongoDBConnectionOptions(BaseModel):

    MIN_POOL_SIZE: int = Field(...)
    MAX_POOL_SIZE: int = Field(...)

class MongoDBDatabase(BaseModel):

    DATABASE_NAME: str = Field(...)
    PASSWORD: str = Field(...)
    USER: str = Field(...)
    HOST: str = Field(...)
    PORT: int = Field(...)

    CONN_OPTS: MongoDBConnectionOptions

    COLLECTIONS: dict = {
        "translation_request": {
            "name": "translation_request"
        },
        "translation_request_result": {
            "name": "translation_request_result"
        },
        "translation_history": {
            "name": "translation_history"
        }
    }

    @property
    def MONGODB_URI(self):

        return 'mongodb://{}:{}@{}:{}/{}'.format(
            self.USER,
            self.PASSWORD,
            self.HOST,
            self.PORT,
            self.DATABASE_NAME
        )
