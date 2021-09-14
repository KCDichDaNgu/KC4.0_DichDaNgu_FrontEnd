from pydantic import PrivateAttr, BaseModel, Field
from typing import Any, Generic, Optional, TypeVar, Union, Final

T = TypeVar('T')

class ValueObjectProps(Generic[T]):

    def __init__(self, value: Union[T, None]):
        self.value = value

class ValueObject(BaseModel, Generic[T]):

    __props: ValueObjectProps[T] = PrivateAttr(...)

    def __init__(self, props: ValueObjectProps[T], **data) -> None:

        super().__init__(**data)
        
        self.__props = props

    @property
    def props(self):
        return self.__props

    @property
    def value(self):
        return self.__props.value

from uuid import uuid4

class ID(ValueObject[str]):

    def __init__(self, value: str):
        super().__init__(ValueObjectProps[str](value))

    @property
    def value(self) -> str:
        return self.props.value

    @staticmethod
    def generate():
        return ID(str(uuid4()))

class TranslationRequestResultProps(BaseModel):
    
    task_id: ID = Field(...)

a = TranslationRequestResultProps(task_id=ID(str(uuid4())))

print(a)
print(a.task_id.value)
