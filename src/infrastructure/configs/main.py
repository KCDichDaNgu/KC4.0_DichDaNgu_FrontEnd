from pathlib import Path
from pydantic import (
    Field,
    BaseSettings,
    BaseModel
)

from typing import Any, Dict, Optional, Union
from enum import unique

from pydantic.networks import AnyHttpUrl
from umongo.frameworks import MotorAsyncIOInstance, PyMongoInstance
from uvicorn.importer import import_from_string
from core.types import ExtendedEnum

from infrastructure.configs.database import CassandraDatabase, MongoDBDatabase
from infrastructure.configs.event_dispatcher import KafkaConsumer, KafkaProducer

import os

@unique
class EnvStateEnum(str, ExtendedEnum):

    dev = 'dev'
    prod = 'prod'

@unique
class ServerTypeEnum(str, ExtendedEnum):

    uvicorn = 'uvicorn'
    built_in = 'built_in'

@unique
class StatusCodeEnum(int, ExtendedEnum):

    success = 1
    failed = 0

@unique
class BackgroundTaskTriggerEnum(str, ExtendedEnum):

    interval = 'interval'
    cron = 'cron'
    date = 'date'

class BackgroundTask(BaseModel):

    ID: str 
    TRIGGER: BackgroundTaskTriggerEnum
    CONFIG: Dict

    class Config:
        use_enum_values = True

class AppConfig(BaseModel):

    APP_NAME: str = 'translation-backend'

    ROUTES: Dict = {
        'translation_request': {
            'path': '/',
            'name': 'Translation request',
        },
        'translation_request.text_translation.create': {
            'path': 'translate',
            'name': 'Create text translation request',
            'summary': 'Create text translation request',
            'desc': 'Create text translation request',
            'method': 'POST'
        },
        'translation_request.doc_translation.create': {
            'path': 'translate_f',
            'name': 'Create document translation request',
            'summary': 'Create document translation request',
            'desc': 'Create document translation request',
            'method': 'POST'
        }
    }

    API_BASEPATH: str = '/api'
    API_VERSION: str = '0.0.1'

    STRICT_SLASHES = False

    BACKGROUND_TASKS: Dict[str, BackgroundTask] = {
        'translate_plain_text_in_public.call_language_detection_service': BackgroundTask(
            ID='translate_plain_text_in_public.call_language_detection_service',
            TRIGGER=BackgroundTaskTriggerEnum.interval.value,
            CONFIG=dict(seconds=3)
        )
    }

class TranslationAPI(BaseModel):

    URL: AnyHttpUrl = Field(...)
    METHOD: str = Field(...)
    ALLOWED_CONCURRENT_REQUEST: int = Field(...) 

class LanguageDetectionAPI(BaseModel):

    URL: AnyHttpUrl = Field(...)
    METHOD: str = Field(...)
    ALLOWED_CONCURRENT_REQUEST: int = Field(...) 

class GlobalConfig(BaseSettings):

    """Global configurations."""

    APP_CONFIG: AppConfig = AppConfig()

    # define global variables with the Field class
    ENV_STATE: Optional[EnvStateEnum] = EnvStateEnum.dev.value

    APP_HOST: str = '0.0.0.0'
    APP_PORT: int = 8000
    APP_DEBUG: bool = False
    APP_WORKERS: int = 1
    ACCESS_LOG: bool = False
    APP_LIFESPAN: str = None
    SERVER_TYPE: str = None

    CQLENG_ALLOW_SCHEMA_MANAGEMENT: Any = Field(env='CQLENG_ALLOW_SCHEMA_MANAGEMENT')

    CASSANDRA_DATABASE: CassandraDatabase 
    MONGODB_DATABASE: MongoDBDatabase

    KAFKA_CONSUMER: KafkaConsumer
    KAFKA_PRODUCER: KafkaProducer

    PRIVATE_TRANSLATION_API: TranslationAPI
    PRIVATE_LANGUAGE_DETECTION_API: LanguageDetectionAPI

    PUBLIC_TRANSLATION_API: TranslationAPI
    PUBLIC_LANGUAGE_DETECTION_API: LanguageDetectionAPI

    class Config:
        """Loads the dotenv file."""

        env_file = ".env"
        env_prefix = 'SANIC_'
        env_file_encoding = 'utf-8'

    def _build_values(
        self, 
        init_kwargs: Dict[str, Any], 
        _env_file: Union[Path, str, None], 
        _env_file_encoding: Optional[str], 
        _secrets_dir: Union[Path, str, None]
    ) -> Dict[str, Any]:
        
        if os.getenv('CQLENG_ALLOW_SCHEMA_MANAGEMENT') is None:
            os.environ['CQLENG_ALLOW_SCHEMA_MANAGEMENT'] = '1'

        return super()._build_values(init_kwargs, _env_file=_env_file, _env_file_encoding=_env_file_encoding, _secrets_dir=_secrets_dir)

class DevConfig(GlobalConfig):
    """Development configurations."""

    APP_DEBUG = True

    class Config:
        env_file = ".env.development"


class ProdConfig(GlobalConfig):
    """Production configurations."""

    APP_DEBUG = False

    class Config:
        env_file = ".env.production"

def update_cnf(new_config):

    ConfigStore.GLOBAL_CNF = new_config

    return ConfigStore.GLOBAL_CNF

def get_cnf() -> GlobalConfig:

   return ConfigStore.GLOBAL_CNF

def update_mongodb_instance(ins):
    
    ConfigStore.MONGODB_INS = ins
    
    return ConfigStore.MONGODB_INS

def get_mongodb_instance():

    return ConfigStore.MONGODB_INS

class ConfigStore:

    GLOBAL_CNF: GlobalConfig = None
    MONGODB_INS: Union[MotorAsyncIOInstance, PyMongoInstance] = None

class FactoryConfig:
    """Returns a config instance dependending on the ENV_STATE variable."""

    def __init__(self, env_state: Optional[str], override_config: Optional[dict]):
        self.env_state = env_state
        self.override_config = override_config

    def __call__(self):

        config = None

        if self.env_state == EnvStateEnum.dev.value:
            config = DevConfig(**self.override_config)
            config.ENV_STATE = EnvStateEnum.dev.value

        elif self.env_state == EnvStateEnum.prod.value:
            config = ProdConfig(**self.override_config)
            config.ENV_STATE = EnvStateEnum.prod.value

        else:
            config = DevConfig(**self.override_config)
            config.ENV_STATE = EnvStateEnum.dev.value

        update_cnf(config)

        return config
