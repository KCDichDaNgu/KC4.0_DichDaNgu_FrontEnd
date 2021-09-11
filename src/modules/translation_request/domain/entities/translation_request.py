from src.core.base_classes.entity import BaseEntityProps
from typing import Union
from pydantic.fields import Field
from pydantic.main import BaseModel
from infrastructure.configs.translation_request import (
    TaskType, CreatorType, Status, TranslationStep, DetectionLanguageStep
)

from core.base_classes.aggregate_root import AggregateRoot
from core.value_objects import DateVO, ID

class TranslationRequestProps(BaseModel):

    creator_id: ID = Field(...)
    task_type: TaskType = Field(...)
    creator_type: CreatorType = Field(...)
    status: Status = Field(...)
    current_step: Union[TranslationStep, DetectionLanguageStep] = Field(...)
    expired_date: DateVO

    class Config:
        use_enum_values = True


class TranslationRequestEntity(AggregateRoot[TranslationRequestProps]):

    def __init__(
        self,
        props: TranslationRequestProps
    ) -> None:
        super().__init__(props)

    class MergedProps(TranslationRequestProps, BaseEntityProps):
        pass

    def get_props_copy(self) -> MergedProps:

        props_copy = {
            'id': self.__id,
            'created_at': self.__created_at,
            'updated_at': self.__updated_at,
            **self.props
        }

        return props_copy
