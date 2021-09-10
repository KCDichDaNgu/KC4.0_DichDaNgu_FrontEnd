from pydantic.fields import PrivateAttr
from pydantic.main import BaseModel
from core.base_classes.value_object import ValueObject, ValueObjectProps
from core.value_objects import DateVO, ID

class TranslationRequestResultProps(BaseModel):
    
    id: ID
    task_id: ID
    step: str
    result_url: str
    created_at: DateVO
    updated_at: DateVO

class TranslationRequestResult(ValueObject[TranslationRequestResultProps]):

    __id: ID = PrivateAttr()
    __created_at: DateVO = PrivateAttr()
    __updated_at: DateVO = PrivateAttr()

    def __init__(self, props: ValueObjectProps[TranslationRequestResultProps]) -> None:
        super().__init__(props)

    @property
    def id(self):

        return self.__id

    @property
    def created_at(self):

        return self.__created_at

    @property
    def updated_at(self):

        return self.__updated_at
