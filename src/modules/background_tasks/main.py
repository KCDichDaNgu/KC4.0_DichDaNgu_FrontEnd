from infrastructure.configs.main import GlobalConfig
from infrastructure.adapters.background_task_manager.main import BackgroundTaskManager
from apscheduler.schedulers.asyncio import AsyncIOScheduler

def init_background_tasks(config: GlobalConfig):
    from modules.background_tasks.tranlate_file_created_by_public_request.detect_content_language.main import main as detect_content_language_for_file_in_public_request
    from modules.background_tasks.tranlate_plain_text_created_by_public_request.detect_content_language.main import main as detect_content_language_for_plain_text_in_public_request
    from modules.background_tasks.tranlate_plain_text_created_by_public_request.translate_content.main import main as translate_content_for_plain_text_in_public_request
    from modules.background_tasks.tranlate_file_created_by_public_request.translate_content.main import main as translate_content_for_file_in_public_request
   

    from modules.background_tasks.detect_plain_text_language_created_by_public_request.main import main as detect_plain_text_language_created_by_public_request
    from modules.background_tasks.detect_file_language_created_by_public_request.main import main as detect_file_language_created_by_public_request
    from modules.background_tasks.delete_invalid_task.main import main as delete_invalid_task
    from modules.background_tasks.delete_invalid_file.main import main as delete_invalid_file

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
    
    background_task_3_conf = BACKGROUND_TASKS['detect_plain_text_language_in_public_request']

    new_background_task_scheduler.add_job(
        detect_plain_text_language_created_by_public_request,
        id=background_task_3_conf.ID,
        trigger=background_task_3_conf.TRIGGER,
        **background_task_3_conf.CONFIG
    )
    
    background_task_4_conf = BACKGROUND_TASKS['delete_invalid_task']
 
    new_background_task_scheduler.add_job(
        delete_invalid_task,
        id=background_task_4_conf.ID,
        trigger=background_task_4_conf.TRIGGER,
        **background_task_4_conf.CONFIG
    )
    
    background_task_5_conf = BACKGROUND_TASKS['delete_invalid_file']
 
    new_background_task_scheduler.add_job(
        delete_invalid_file,
        id=background_task_5_conf.ID,
        trigger=background_task_5_conf.TRIGGER,
        **background_task_5_conf.CONFIG
    )

    background_task_6_conf = BACKGROUND_TASKS['translate_content_for_file_in_public_request.translate_content']
 
    new_background_task_scheduler.add_job(
        translate_content_for_file_in_public_request,
        id=background_task_6_conf.ID,
        trigger=background_task_6_conf.TRIGGER,
        **background_task_6_conf.CONFIG
    )

    background_task_7_conf = BACKGROUND_TASKS['detect_file_language_created_by_public_request']
 
    new_background_task_scheduler.add_job(
        detect_file_language_created_by_public_request,
        id=background_task_7_conf.ID,
        trigger=background_task_7_conf.TRIGGER,
        **background_task_7_conf.CONFIG
    )

    background_task_8_conf = BACKGROUND_TASKS['translate_content_for_file_in_public_request.detect_content_language']
 
    new_background_task_scheduler.add_job(
        detect_content_language_for_file_in_public_request,
        id=background_task_8_conf.ID,
        trigger=background_task_8_conf.TRIGGER,
        **background_task_8_conf.CONFIG
    )
