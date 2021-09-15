from infrastructure.configs.main import GlobalConfig
from infrastructure.adapters.background_task_manager.main import BackgroundTaskManager
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from modules.background_tasks.tranlate_plain_text_in_public.call_language_detection_service.main import main as tranlate_plain_text_in_public_call_language_detection_service

def init_background_tasks(config: GlobalConfig):
    
    BACKGROUND_TASKS = config.APP_CONFIG.BACKGROUND_TASKS

    new_background_task_scheduler = BackgroundTaskManager(AsyncIOScheduler())
    
    background_task_1_conf = BACKGROUND_TASKS['translate_plain_text_in_public.call_language_detection_service']

    new_background_task_scheduler.remove_all_jobs()

    new_background_task_scheduler.add_job(
        tranlate_plain_text_in_public_call_language_detection_service,
        id=background_task_1_conf.ID,
        trigger=background_task_1_conf.TRIGGER,
        **background_task_1_conf.CONFIG
    )
    