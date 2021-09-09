from pydantic.fields import PrivateAttr
from core.exceptions import ArgumentNotProvidedException
from core.guard import Guard
from core.utils import convert_props_to_object
from numbers import Complex
from typing import Any, Generic, Optional, TypeVar, Union, Final
from abc import ABC, abstractmethod
from pydantic import BaseModel

from datetime import datetime

Primitives = Union[str, Complex, bool]

T = TypeVar('T', Primitives, datetime)

class DomainPrimitive(Generic(T)):

    def __init__(self, value: T):
        self.value = value

class ValueObjectProps(Generic[T]):

    def __init__(self, value: T):
        self.value = value

class ValueObject(BaseModel, ABC, Generic[T]):

    __props: ValueObjectProps[T] = PrivateAttr()

    def __init__(self, props: ValueObjectProps[T]) -> None:
        
        self.__props = props

        self.check_if_empty(props)
        self.validate(props)

    @property
    def props(self):
        return self.__props

    @abstractmethod
    def validate(props: ValueObjectProps[T]):
        ...
    
    @staticmethod
    def is_value_object(obj):
        return isinstance(obj, ValueObject)

    def equals(self, vo: Optional[Any]) -> bool:
        if vo is None:
            return False
        
        return vo.props.value == self.props.value

    def get_raw_props(self) -> T:

        if self.is_domain_primitive(self.__props):
            return self.__props.value

        props_copy: Final = convert_props_to_object(self.__props)

        return props_copy

    def check_if_empty(self, props: ValueObjectProps[T]):

        if Guard.is_empty(props) or \
            self.is_domain_primitive(props) and Guard.is_empty(props.value):
            raise ArgumentNotProvidedException('Property cannot be empty')

    def is_domain_primitive(obj: Any):

        if hasattr(obj, 'value') and isinstance(obj.value, Primitives.__args__):
            return True

        return False