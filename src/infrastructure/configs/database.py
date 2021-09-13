from typing import Any
from pydantic import BaseModel, Field

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

    KEYSPACE: KeySpaceConfig = KeySpaceConfig()
    
    PROTOCOL_VERSION: int = 3

    TABLES: dict = {
        "translation_request": {
            "name": "translation_request"
        },
        "translation_request_result": {
            "name": "translation_request_result"
        }
    }
