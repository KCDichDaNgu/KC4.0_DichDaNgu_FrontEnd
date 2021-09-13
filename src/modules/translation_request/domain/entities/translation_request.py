from pydantic.class_validators import validator
from core.base_classes.entity import BaseEntityProps
from typing import Union
from pydantic import Field, BaseModel
from infrastructure.configs.translation_request import (
    TaskTypeEnum, CreatorTypeEnum, StatusEnum, TranslationStepEnum, DetectionLanguageStepEnum, private_tasks
)

from addict import Addict

from core.base_classes.aggregate_root import AggregateRoot
from core.value_objects import DateVO, ID

class TranslationRequestProps(BaseModel):

    creator_id: Union[ID, None] = None
    task_type: TaskTypeEnum = Field(...)
    creator_type: CreatorTypeEnum = Field(...)
    status: StatusEnum = Field(...)
    current_step: Union[TranslationStepEnum, DetectionLanguageStepEnum] = Field(...)
    expired_date: DateVO

    class Config:
        use_enum_values = True

    @validator('creator_id')
    def validate(cls, v, values, **kwargs):

        if values['task_type'] in private_tasks and not v:
            raise ValueError('Creator cannot be None')
            
        return v

class TranslationRequestEntity(AggregateRoot[TranslationRequestProps]):

    pass
