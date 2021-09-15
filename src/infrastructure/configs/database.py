from typing import Any
from pydantic import BaseModel, Field
from umongo import MotorAsyncIOInstance

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

    KEYSPACE: KeySpaceConfig = KeySpaceConfig()
    
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

class MongoDBDatabase(BaseModel):

    DATABASE_NAME: str = Field(None)
    PASSWORD: str = Field(None)
    USER: str = Field(None)
    HOST: str = Field(None)
    PORT: int = Field(None)

    LAZY_UMONGO = MotorAsyncIOInstance()

    @property
    def MONGODB_URI(self):

        return 'mongodb://{}:{}@{}:{}/{}'.format(
            self.USER,
            self.PASSWORD,
            self.HOST,
            self.PORT,
            self.DATABASE_NAME
        )
