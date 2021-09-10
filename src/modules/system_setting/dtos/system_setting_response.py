from src.core.value_objects.date import DateVO
from pydantic.fields import Field
from src.core.value_objects.id import ID


class SystemSettingDto():
    
    editor_id: ID = Field(...)
    max_translate_text_per_day: int = Field(...)
    max_translate_doc_per_day: int = Field(...)
    translation_history_expire_duration: DateVO