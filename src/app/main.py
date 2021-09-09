from sanic import Sanic
from infrastructure.configs.main import GlobalConfig
from infrastructure.database import init_db

from infrastructure.configs import ServerType, get_cnf, GlobalConfig

from infrastructure.interceptors.exeption_interceptor import ExceptionInterceptor
from infrastructure.adapters.kafka.main import init_kafka

async def listener_before_server_start(*args, **kwargs):
    print("before_server_start")
    
async def listener_after_server_start(*args, **kwargs):
    print("after_server_start")
    
async def listener_before_server_stop(*args, **kwargs):    
    print("before_server_stop")
    
async def listener_after_server_stop(*args, **kwargs):
    print("after_server_stop")

async def init_app():
    
    app: Sanic = Sanic('face-recognition-service')
    
    config: GlobalConfig = get_cnf()

    app.config.update_config(config.dict())
    
    init_db(config.CASSANDRA_DATABASE)

    await init_kafka(config)

    app.error_handler = ExceptionInterceptor()

    if config.SERVER_TYPE == ServerType.uvicorn.value:

        app.register_listener(listener_after_server_start, 'after_server_start')
        app.register_listener(listener_before_server_stop, 'before_server_stop')

    elif config.SERVER_TYPE == ServerType.built_in.value:

        app.register_listener(listener_before_server_start, 'before_server_start')
        app.register_listener(listener_after_server_start, 'after_server_start')
        app.register_listener(listener_before_server_stop, 'before_server_stop')
        app.register_listener(listener_after_server_stop, 'after_server_stop')
    
    return app
