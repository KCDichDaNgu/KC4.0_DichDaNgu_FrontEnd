from pydantic.class_validators import validator
from core.base_classes.entity import BaseEntityProps
from typing import Union
from pydantic import Field, BaseModel

from addict import Addict

from core.base_classes.aggregate_root import AggregateRoot
from core.value_objects import DateVO, ID


class SystemSettingProps(BaseModel):

    editor_id: Union[ID, None] = None
    max_translate_text_per_day: int = Field(...)
    max_translate_doc_per_day: int = Field(...)
    translation_history_expire_duration: int = Field(...)

    class Config:
        use_enum_values = True

    @validator('editor_id')
    def validate(cls, v, values, **kwargs):
        return v


class SystemSettingEntity(AggregateRoot[SystemSettingProps]):

    pass
