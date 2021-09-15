from pydantic.class_validators import root_validator
from typing import Union
from pydantic import Field, BaseModel
from infrastructure.configs.translation_request import (
    TaskTypeEnum, CreatorTypeEnum, StepStatusEnum, TranslationStepEnum, DetectionLanguageStepEnum, TRANSLATION_PRIVATE_TASKS
)

from core.base_classes.aggregate_root import AggregateRoot
from core.value_objects import DateVO, ID

class TranslationRequestProps(BaseModel):

    creator_id: ID
    task_type: TaskTypeEnum = Field(...)
    creator_type: CreatorTypeEnum = Field(...)
    step_status: StepStatusEnum = Field(...)
    current_step: Union[TranslationStepEnum, DetectionLanguageStepEnum] = Field(...)
    expired_date: DateVO = DateVO(None)

    class Config:
        use_enum_values = True

    @root_validator(pre=True)
    def validate(cls, values):
        
        if values['task_type'] in TRANSLATION_PRIVATE_TASKS and not values['creator_id'].value:
            raise ValueError('Creator cannot be None')

        return values

class TranslationRequestEntity(AggregateRoot[TranslationRequestProps]):

    pass
