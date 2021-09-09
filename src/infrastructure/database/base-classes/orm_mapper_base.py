from _typeshed import Self
from core.base_classes.entity import BaseEntityProps
from core.value_objects.date import DateVO
from core.value_objects.id import ID
from abc import ABC, abstractmethod
from pydantic import BaseModel
from typing import TypeVar
from entity_base import EntityBase

Entity = TypeVar('Entity')
OrmEntity = TypeVar('OrmEntity')
Props = TypeVar('Props')

class OrmMapper(ABC, Entity(BaseEntityProps), OrmEntity, BaseModel):
    
    def __init__(self) -> None:

        self.__entityConstructor: Entity
        self.__ormEntityConstructor: OrmEntity

    @abstractmethod
    def _toDomainProps(self, ormEntity: OrmEntity) -> Entity:
        return

    @abstractmethod
    def _toOrmEntity(self, entity: Entity) -> OrmEntity:
        return

    def toDomainEntity(self, ormEntity: OrmEntity) -> Entity:
        props = self._toDomainProps(ormEntity)
        return self.assignPropsToEntity(props, ormEntity)

    def toOrmEntity(self, entity: Entity) -> OrmEntity:
        props = self.toOrmEntity(entity)
        return self.__ormEntityConstructor({
            **props,
            'id': entity.id.value,
            'createdAt': entity.createdAt.value,
            'updatedAt': entity.updatedAt.value
        })


    def assignPropsToEntity(
        self, 
        entityProps: Props,
        ormEntity: OrmEntity) -> Entity:

        entityCopy: any = {**self.__entityConstructor}
        ormEntityBase: EntityBase = ormEntity

        entityCopy.props = entityProps
        entityCopy.id = ID(ormEntityBase.id)
        entityCopy.createAt = DateVO(ormEntityBase.createdAt)
        entityCopy.updatedAt = DateVO(ormEntityBase.updatedAt)

        return entityCopy