from pydantic import (
    Field,
    BaseSettings,
    BaseModel
)

from typing import List, Optional
from enum import Enum, unique

CNF = None

@unique
class EnvState(str, Enum):

    dev = 'dev'
    prod = 'prod'

@unique
class ServerType(Enum):

    uvicorn = 'uvicorn'
    built_in = 'built_in'

class CassandraDatabase(BaseModel):

    NAME: str = Field(None)
    PASSWORD: str = Field(None)
    USER: str = Field(None)
    KEYSPACE: str = Field(None)
    HOST: str = Field(None)

class KafkaProducer(BaseModel):

    BOOTSTRAP_SERVERS: List[str] = None
    TOPICS: List[str] = None

class KafkaConsumer(BaseModel):

    BOOTSTRAP_SERVERS: List[str] = None
    TOPICS: List[str] = None
    GROUP: str = Field(None)

class AppConfig(BaseModel):
    """Application configurations."""
    pass

class GlobalConfig(BaseSettings):

    """Global configurations."""

    APP_CONFIG: AppConfig = AppConfig()
    
    # define global variables with the Field class
    ENV_STATE: Optional[EnvState] = EnvState.dev.value

    APP_HOST: str = '0.0.0.0'
    APP_PORT: int = 8000
    APP_DEBUG: bool = False
    APP_WORKERS: int = 1
    ACCESS_LOG: bool = False
    APP_LIFESPAN: str = None
    SERVER_TYPE: str = None

    CASSANDRA_DATABASE: CassandraDatabase = CassandraDatabase()
    KAFKA_CONSUMER: KafkaConsumer = KafkaConsumer()
    KAFKA_PRODUCER: KafkaProducer = KafkaProducer()

    class Config:
        """Loads the dotenv file."""

        env_file = ".env"
        env_prefix = 'SANIC_'
        env_file_encoding = 'utf-8'

class DevConfig(GlobalConfig):
    """Development configurations."""

    APP_DEBUG = True

    CASSANDRA_DATABASE: CassandraDatabase
    KAFKA_CONSUMER: KafkaConsumer
    KAFKA_PRODUCER: KafkaProducer

    class Config:
        env_file = ".env.development"


class ProdConfig(GlobalConfig):
    """Production configurations."""

    APP_DEBUG = False

    class Config:
        env_file = ".env.production"

def update_cnf(new_config):

    import infrastructure.configs
    
    infrastructure.configs.CNF = new_config

def get_cnf() -> GlobalConfig:

    import infrastructure.configs
    
    return infrastructure.configs.CNF
        
class FactoryConfig:
    """Returns a config instance dependending on the ENV_STATE variable."""

    def __init__(self, env_state: Optional[str], override_config: Optional[dict]):
        self.env_state = env_state
        self.override_config = override_config

    def __call__(self):
        
        config = None
        
        if self.env_state == EnvState.dev.value:
            config = DevConfig(**self.override_config)
            config.ENV_STATE = EnvState.dev.value

        elif self.env_state == EnvState.prod.value:
            config = ProdConfig(**self.override_config)
            config.ENV_STATE = EnvState.prod.value

        else: 
            config = DevConfig(**self.override_config)
            config.ENV_STATE = EnvState.dev.value

        update_cnf(config)
        
        return config
