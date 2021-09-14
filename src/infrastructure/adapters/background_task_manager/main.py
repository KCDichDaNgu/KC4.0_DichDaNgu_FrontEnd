from core.ports.background_task_manager import BackgroundTaskManagerPort
from apscheduler.schedulers.asyncio import AsyncIOScheduler

class BackgroundTaskManager(BackgroundTaskManagerPort):

    scheduler: AsyncIOScheduler = None

    def __init__(self, scheduler: AsyncIOScheduler = None, force_assignment: bool = False) -> None:
        
        if self.scheduler is None or force_assignment == True:
            self.scheduler = scheduler

    def start(self):

        self.scheduler.start()

    def stop(self):

        self.scheduler.shutdown()

    def add_job(self, func, **kwargs):
        
        self.scheduler.add_job(func, **kwargs)

    def get_job(self, job_id, **kwargs):

        return self.scheduler.get_job(job_id, **kwargs)

    def get_jobs(self, **kwargs):
        
        return self.scheduler.get_jobs(**kwargs)

    def remove_all_jobs(self, **kwargs):

        return self.scheduler.remove_all_jobs(**kwargs)
