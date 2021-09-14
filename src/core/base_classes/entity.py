from pydantic.fields import Field
from core.base_classes.value_object import ValueObject
from core.exceptions import (
    ArgumentInvalidException, 
    ArgumentNotProvidedException, 
    ArgumentOutOfRangeException
)

from core.guard import Guard
from core.value_objects import DateVO, ID
from addict import Addict
from abc import ABC
from pydantic import BaseModel, PrivateAttr

from typing import Any, Dict, Generic, List, Final, NewType, Optional, TypeVar

EntityProps = TypeVar('EntityProps')

class BaseEntityProps(BaseModel, ABC):

    id: ID
    created_at: DateVO
    updated_at: DateVO

class Entity(BaseModel, Generic[EntityProps], ABC):

    __id: ID = PrivateAttr()
    __created_at: DateVO = PrivateAttr(None)
    __updated_at: DateVO = PrivateAttr(None)
    
    props: EntityProps
        
    def __init__(
        self, 
        props: EntityProps,
        **data
    ) -> None:
        super().__init__(props=props, **data)
    
        self.__id = ID.generate()

        # now: Final = DateVO.now()

        # self.__created_at = now
        # self.__updated_at = now

    class MergedProps(Generic[EntityProps], BaseEntityProps):
        pass

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

    def get_props_copy(self) -> MergedProps:

        props_copy = {
            'id': self.__id.value if self.__id else None,
            'created_at': self.__created_at.value if self.__created_at else None,
            'updated_at': self.__updated_at.value if self.__updated_at else None,
            **self.props.__dict__
        }
                
        return Addict(props_copy)

    @classmethod
    def from_orm(cls, props: Dict):

        new_entity = cls(props)

        if "id" in props:

            new_entity.__id = props["id"]

        if "created_at" in props:

            new_entity.__created_at = props["created_at"]

        if "updated_at" in props:

            new_entity.__updated_at = props["updated_at"]

        return new_entity

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
