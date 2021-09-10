from pydantic.fields import Field
from pydantic.main import BaseModel
from core.base_classes.value_object import ValueObject
from core.value_objects import DateVO, ID

class SystemSettingProps(BaseModel):

    editor_id: ID = Field(...)
    max_translate_text_per_day: int = Field(...)
    max_translate_doc_per_day: int = Field(...)
    translation_history_expire_duration: DateVO


class SystemSetting(ValueObject):
    def __init__(self, props: SystemSettingProps[T]) -> None:
        super().__init__(props)