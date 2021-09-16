from core.value_objects import ID, DateVO
from typing import Any
from infrastructure.database.base_classes.mongodb.orm_mapper_base import OrmMapperBase

from modules.task.database.task_result.orm_entity import TaskResultOrmEntity
from modules.task.domain.entities.task_result import TaskResultEntity, TaskResultProps

class TaskResultOrmMapper(OrmMapperBase[TaskResultEntity, TaskResultOrmEntity]):

    def to_orm_props(self, entity: TaskResultEntity):
        
        props = entity.get_props_copy()
        
        orm_props = {
            'task_id': props.task_id.value,
            'step': props.step,
            'file_path': props.file_path
        }
        
        return orm_props

    def to_domain_props(self, orm_entity: TaskResultOrmEntity):

        props = {
            'task_id': ID(str(orm_entity.task_id)),
            'step': orm_entity.step,
            'file_path': orm_entity.file_path
        }

        return props
