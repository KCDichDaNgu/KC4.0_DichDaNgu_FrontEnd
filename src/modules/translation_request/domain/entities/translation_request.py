from pydantic.class_validators import root_validator
from typing import Union
from pydantic import Field
from infrastructure.configs.task import (
    TranslationTaskStepEnum, LanguageDetectionTaskStepEnum, TRANSLATION_PRIVATE_TASKS
)

from core.base_classes.aggregate_root import AggregateRoot

from modules.task.domain.entities.task import TaskEntity, TaskProps

from typing import get_args

class TranslationRequestProps(TaskProps):

    current_step: Union[TranslationTaskStepEnum, LanguageDetectionTaskStepEnum] = Field(...)

    @root_validator(pre=True)
    def validate(cls, values):
        
        if values['task_name'] in TRANSLATION_PRIVATE_TASKS and not values['creator_id'].value:
            raise ValueError('Creator cannot be None')

        return values

class TranslationRequestEntity(TaskEntity, AggregateRoot[TranslationRequestProps]):

    @property
    def props_klass(self):
        return get_args(self.__orig_bases__[1])[0]
