from core.base_classes.entity import BaseEntityProps
from core.value_objects import DateVO, ID
from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar
from infrastructure.database.base_classes.orm_entity_base import OrmEntityBase

Entity = TypeVar('Entity', BaseEntityProps)
OrmEntity = TypeVar('OrmEntity')
Props = TypeVar('Props')

class OrmMapper(ABC, Generic[Entity, OrmEntity]):
    
    def __init__(self) -> None:
        pass

    @abstractmethod
    def to_domain_props(self, orm_entity: OrmEntity) -> Any:
        return

    @abstractmethod
    def to_orm_entity(self, entity: Entity) -> OrmEntity:
        return

    def to_domain_entity(self, orm_entity: OrmEntity) -> Entity:

        props = self.to_domain_props(orm_entity)

        return self.assign_props_to_entity(props, orm_entity)

    def to_orm_entity(self, entity: Entity) -> OrmEntity:

        props = self.to_orm_entity(entity)

        return OrmEntityBase(**{
            **props,
            'id': entity.id.value,
            'created_at': entity.created_at.value,
            'updated_at': entity.updated_at.value
        })


    def assign_props_to_entity(
        self, 
        entity_props: Any,
        orm_entity: OrmEntity
    ) -> Entity:

        orm_entity_base: OrmEntityBase = orm_entity

        return Entity.from_orm({
            **entity_props,
            "id": ID(orm_entity_base.id),
            "created_at": DateVO(orm_entity_base.created_at),
            "updated_at": DateVO(orm_entity_base.updated_at)
        })
