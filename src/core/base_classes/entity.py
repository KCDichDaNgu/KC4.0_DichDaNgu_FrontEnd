from core.base_classes.value_object import ValueObject
from core.exceptions import (
    ArgumentInvalidException, 
    ArgumentNotProvidedException, 
    ArgumentOutOfRangeException
)

from core.guard import Guard
from core.value_objects.date import DateVO
from core.value_objects.id import ID

from abc import ABC
from pydantic import BaseModel, PrivateAttr

from typing import Any, List, Final, Optional, TypeVar, Union

EntityProps = TypeVar('EntityProps')

class BaseEntityProps(BaseModel, ABC):

    id: ID
    created_at: DateVO
    updated_at: DateVO


class Entity(BaseModel, EntityProps, ABC):

    __id: ID = PrivateAttr()
    __created_at: DateVO = PrivateAttr()
    __updated_at: DateVO = PrivateAttr()
    
    props: EntityProps

    def __init__(self, props: EntityProps) -> None:
        self.validate_props(props)
        self.__id = ID.generate()

        now: Final = DateVO.now()
        self.__created_at = now
        self.__updated_at = now

        self.props = props

    @property
    def props(self):

        return self.props

    @property
    def id(self) -> ID:

        return self.__id 

    @property
    def created_at(self) -> DateVO:

        return self.__created_at

    @property
    def updated_at(self) -> DateVO:

        return self.__updated_at

    @staticmethod
    def is_entity(entity: Any):

        return isinstance(entity, Entity)

    def equals(self, object: Optional[Any]):

        if object is None:
            return False

        if not Entity.is_entity(object):
            return False

        return self.__id if self.__id == object.id else False

    def get_props_copy(self) -> Union[EntityProps, BaseEntityProps]:

        props_copy = {
            'id': self.__id,
            'created_at': self.__created_at,
            'updated_at': self.__updated_at,
            **self.props
        }

        return props_copy

    @staticmethod
    def convert_to_raw(item: Any):

        if ValueObject.is_value_object(item):
            return item.get_raw_props()
        
        if Entity.is_entity(item):
            return item.to_object()

        return item
    
    @staticmethod
    def convert_props_to_object(props: Any) -> Any:

        props_copy = { **props }

        for prop in props_copy:

            if isinstance(props_copy[prop], List):

                props_copy[prop] = list(map(lambda item: Entity.convert_to_raw(item), props_copy[prop]))

            props_copy[prop] = Entity.convert_to_raw(props_copy[prop])

        return props_copy

    def to_object(self) -> Any:

        props_copy = Entity.convert_props_to_object(self.props)

        return {
            'id': self.__id,
            'created_at': self.__created_at.value,
            'updated_at': self.__updated_at.value,
            **props_copy
        }

    def validate_props(self, props: EntityProps):

        max_props = 50

        if Guard.is_empty(props):
            raise ArgumentNotProvidedException(
                'Entity props should not be empty'
            )
        
        if props is not dict:
            raise ArgumentInvalidException(
                'Entity props should be an object'
            ) 

        if len(list(object.keys())) > max_props:
            raise ArgumentOutOfRangeException(
                f'Entity props should not have more then {max_props} properties'
            )
