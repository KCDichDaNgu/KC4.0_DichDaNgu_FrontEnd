from time import time
from pydantic import Field
from typing import Optional

from core.base_classes.entity import Entity
from core.value_objects import ID

from modules.task.domain.entities.task_result import TaskResultEntity, TaskResultProps

from typing import get_args

class TranslationRequestResultProps(TaskResultProps):
    
    task_id: ID = Field(...)
    step: str = Field(...)
    file_path: Optional[str]

class TranslationRequestResultEntity(
    TaskResultEntity, 
    Entity[TranslationRequestResultProps]
):

    @property
    def props_klass(self):
        return get_args(self.__orig_bases__[1])[0]
