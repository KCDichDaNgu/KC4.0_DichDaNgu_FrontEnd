from pydantic.main import BaseModel
from core.base_classes.value_object import ValueObject
from core.value_objects import DateVO, ID

class TranslationRequestResultProps(BaseModel):
    
    task_id: ID
    step: str
    result_url: str

class TranslationRequestResult(ValueObject):
    def __init__(self, props: TranslationRequestResultProps[T]) -> None:
        super().__init__(props)