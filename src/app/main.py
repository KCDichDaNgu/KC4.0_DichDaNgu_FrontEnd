from typing import List
from sanic import Sanic, config
from infrastructure.configs.main import GlobalConfig
from sanic_openapi import swagger_blueprint

from infrastructure.configs import ServerTypeEnum, get_cnf, GlobalConfig
from infrastructure.configs.task import TASK_RESULT_FOLDER
from infrastructure.interceptors.exeption_interceptor import ExceptionInterceptor

import os, aiofiles

async def listener_before_server_start(*args, **kwargs):
    print("before_server_start")
    
async def listener_after_server_start(*args, **kwargs):

    from infrastructure.configs.main import get_cnf
    from infrastructure.database.main import init_mongodb
    from modules.background_tasks.main import init_background_tasks
    from infrastructure.adapters.background_task_manager.main import BackgroundTaskManager

    config = get_cnf()

    init_mongodb(config.MONGODB_DATABASE)

    init_background_tasks(config)

    BackgroundTaskManager.scheduler.start()

    print("after_server_start")
    
async def listener_before_server_stop(*args, **kwargs): 

    from infrastructure.adapters.background_task_manager.main import BackgroundTaskManager

    BackgroundTaskManager.scheduler.stop()
    
async def listener_after_server_stop(*args, **kwargs):
    print("after_server_stop")

def init_routes(app: Sanic) -> Sanic:

    from modules.translation_request.main import translation_request_bp
    from modules.translation_history.main import translation_history_bp

    from modules.language_detection_request.main import language_detection_request_bp
    from modules.language_detection_history.main import language_detection_history_bp

    from modules.static_files_server.main import static_files_server_bp

    app.blueprint(swagger_blueprint)

    app.blueprint(translation_request_bp)
    app.blueprint(translation_history_bp)

    app.blueprint(language_detection_request_bp)
    app.blueprint(language_detection_history_bp)

    app.blueprint(static_files_server_bp)
    
    return app

async def mkdir_required_folders(folders_path: List[str]):

    for folder_path in folders_path:

        if not os.path.exists(folder_path):
            await aiofiles.os.mkdir(folder_path)

async def init_app():

    config: GlobalConfig = get_cnf()
    
    app: Sanic = Sanic(
        config.APP_CONFIG.APP_NAME, 
        strict_slashes=config.APP_CONFIG.STRICT_SLASHES
    )
    
    app.config.update_config(config.dict())
    
    await mkdir_required_folders([
        TASK_RESULT_FOLDER
    ])

    # await init_kafka(config)

    init_routes(app)

    app.error_handler = ExceptionInterceptor()

    if config.SERVER_TYPE == ServerTypeEnum.uvicorn.value:

        app.register_listener(listener_after_server_start, 'after_server_start')
        app.register_listener(listener_before_server_stop, 'before_server_stop')

    elif config.SERVER_TYPE == ServerTypeEnum.built_in.value:

        app.register_listener(listener_before_server_start, 'before_server_start')
        app.register_listener(listener_after_server_start, 'after_server_start')
        app.register_listener(listener_before_server_stop, 'before_server_stop')
        app.register_listener(listener_after_server_stop, 'after_server_stop')
    
    return app