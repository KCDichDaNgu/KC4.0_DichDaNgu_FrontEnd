from modules.task.database.task_result.orm_mapper import TaskResultOrmMapper
from modules.task.database.task_result.orm_entity import TaskResultOrmEntity
from core.ports.repository import RepositoryPort
from modules.task.domain.entities.task_result import TaskResultEntity, TaskResultProps
from infrastructure.database.base_classes.mongodb.orm_repository_base import OrmRepositoryBase

class TasktResultRepositoryPort(
    RepositoryPort[
        TaskResultEntity, 
        TaskResultProps
    ]):

    pass

class TasktResultRepository(
    OrmRepositoryBase[
        TaskResultEntity, 
        TaskResultProps, 
        TaskResultOrmEntity,
        TaskResultOrmMapper
    ], 
    TasktResultRepositoryPort
):

    pass
