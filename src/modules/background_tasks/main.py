from infrastructure.configs.main import GlobalConfig
from infrastructure.adapters.background_task_manager.main import BackgroundTaskManager
from apscheduler.schedulers.asyncio import AsyncIOScheduler

def init_background_tasks(config: GlobalConfig):

    from modules.background_tasks.tranlate_plain_text_created_by_public_request.detect_content_language.main import main as detect_content_language_for_plain_text_in_public_request
    from modules.background_tasks.tranlate_plain_text_created_by_public_request.translate_content.main import main as translate_content_for_plain_text_in_public_request
    
    BACKGROUND_TASKS = config.APP_CONFIG.BACKGROUND_TASKS

    new_background_task_scheduler = BackgroundTaskManager(AsyncIOScheduler())

    new_background_task_scheduler.remove_all_jobs()
    
    background_task_1_conf = BACKGROUND_TASKS['translate_plain_text_in_public_request.detect_content_language']

    new_background_task_scheduler.add_job(
        detect_content_language_for_plain_text_in_public_request,
        id=background_task_1_conf.ID,
        trigger=background_task_1_conf.TRIGGER,
        **background_task_1_conf.CONFIG,
    )

    background_task_2_conf = BACKGROUND_TASKS['translate_plain_text_in_public_request.translate_content']

    new_background_task_scheduler.add_job(
        translate_content_for_plain_text_in_public_request,
        id=background_task_2_conf.ID,
        trigger=background_task_2_conf.TRIGGER,
        **background_task_2_conf.CONFIG
    )
