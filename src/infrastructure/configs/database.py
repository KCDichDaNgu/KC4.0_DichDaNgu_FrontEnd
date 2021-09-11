from pydantic import BaseModel, Field

class CassandraDatabase(BaseModel):
    
    NAME: str = Field(None)
    PASSWORD: str = Field(None)
    USER: str = Field(None)
    KEYSPACE: str = Field(None)
    HOST: str = Field(None)

    TABLES: dict = {
        "translation_request": {
            "name": "translation_request"
        },
        "translation_request_result": {
            "name": "translation_request_result"
        }
    }
