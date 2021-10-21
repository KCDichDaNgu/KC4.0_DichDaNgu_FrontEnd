from pydantic.class_validators import root_validator
from typing import Union
from pydantic import Field
from infrastructure.configs.task import (
    SpeechRecognitionTaskStepEnum,
    SpeechRecognitionTaskNameEnum,
)

from core.base_classes.aggregate_root import AggregateRoot

from modules.task.domain.entities.task import TaskEntity, TaskProps

from typing import get_args

class SpeechRecognitionRequestProps(TaskProps):
    current_step: Union[SpeechRecognitionTaskStepEnum] = Field(...)
    task_name: Union[SpeechRecognitionTaskNameEnum] = Field(...)

    @root_validator(pre=True)
    def validate(cls, values):
        if values['task_name'] == SpeechRecognitionTaskNameEnum.private_speech_recognition and not values[
            'creator_id'].value:
            raise ValueError('Creator cannot be None')

        return values

class SpeechRecognitionRequestEntity(TaskEntity, AggregateRoot[SpeechRecognitionRequestProps]):

    @property
    def props_klass(self):
        return get_args(self.__orig_bases__[1])[0]
