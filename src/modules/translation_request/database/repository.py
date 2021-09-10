from modules.user_request.database.entity import TaskResult, Task
from infrastructure.database.base_classes.repository_base import RepositoryBase

class UserRequestRepository(RepositoryBase):
    def __init__(self) -> None:
        super(UserRequestRepository).__init__()

    def create_task(task_entity):
        data = TaskResult.create(step=1, result_url="")
        return data

    def create_detect_language_task(params):
        entity = Task.create(creator_type="user", type="detectingLanguage", status="not_yet_processed")
        return entity

    
