from infrastructure.database.base_classes.mongodb import OrmMapperBase, OrmEntityBase

from typing import NewType, TypeVar
from core.value_objects.id import ID
from core.domain_events import DomainEvents
from infrastructure.adapters.logger import Logger
from core.ports.repository import RepositoryPort, DataWithPaginationMeta
from core.exceptions import NotFoundException

from core.base_classes.entity import BaseEntityProps
from abc import ABC
from typing import Generic, List, TypeVar, Any, Union

import asyncio

Entity = TypeVar('Entity', bound=BaseEntityProps)
EntityProps = TypeVar('EntityProps')
OrmEntity = TypeVar('OrmEntity', bound=OrmEntityBase)
OrmMapper = TypeVar('OrmMapper', bound=OrmMapperBase)

class OrmRepositoryBase(
    Generic[Entity, EntityProps, OrmEntity, OrmMapper], 
    RepositoryPort[Entity, EntityProps],
    ABC
):

    def __init__(
        self,
        repository: OrmEntityBase = None,
        mapper: OrmMapperBase = None,
        table_name: str = None
    ) -> None:

        self.__table_name__ = table_name
        
        self.__repository = repository

        self.__mapper: OrmMapperBase = mapper

        self.__logger: Logger = Logger(__name__)

        self.__relations: List[str] = []

    @property
    def mapper(self):
        return self.__mapper

    @property
    def logger(self):
        return self.__logger

    @property
    def repository(self):
        return self.__repository

    @property
    def table_name(self):
        return self.__table_name__

    @property
    def relations(self):
        return self.__relations
        
    async def create(self, entity: Entity):
        
        orm_entity = self.__mapper.to_orm_entity(entity)
        
        await DomainEvents.publish_events(entity.id, self.__logger)
        
        new_data = self.__repository(
            **(orm_entity.dump())
        )
        
        new_data.commit()

        self.__logger.debug(f'[Entity persisted]: {type(entity).__name__} {entity.id}')
        
        return self.__mapper.to_domain_entity(new_data)

    async def update(self, entity: Entity):

        orm_entity = self.__mapper.to_orm_entity(entity)
        
        await DomainEvents.publish_events(entity.id, self.__logger)
        
        result = await self.__repository.update(
            **(orm_entity.dump())
        ).commit()

        self.__logger.debug(f'[Entity persisted]: {type(entity).__name__} {entity.id}')
        
        return self.__mapper.to_domain_entity(result)

    async def find_one(
        self,
        **params: Any,
    ):

        found = self.__repository.find_one(**params)

        return self.__mapper.to_domain_entity(found) if found else None

    async def find_one_or_throw(self, params: Any = {}):
        
        found = None

        try:
            found = await self.find_one(**params)
        
        except NotFoundException:
            print('Not found')

        return found
            

    async def find_one_by_id_or_throw(self, id: Union[ID, str]):

        try:
            found = await self.find_one(id=id)

        except NotFoundException:
            print('Not found')

        return found

    async def find_many(
        self, 
        params: Any, 
        skip: int = None, 
        limit: int = None,
        order_by: Any = None
    ):
        
        result = []
        
        cursor = self.__repository.find(params)

        if skip:
            cursor = cursor.skip(limit)

        if limit:
            cursor = cursor.limit(limit)

        if order_by:
            cursor = cursor.sort(limit)

        for a in cursor:
            print(a)
        # result = list(map(lambda found: self.__mapper.to_domain_entity(found), founds))

        return result  

    async def find_many_paginated(
        self,
        options: Any
    ):
        
        result = []

        founds = await self.__repository.async_filter(options.params)
        
        count = founds.count()

        founds = founds[options.pagination.skip : options.pagination.limit]
        founds = founds.order_by(options.order_by)

        for found in founds:
            result.append(self.__mapper.to_domain_entity(found))

        return DataWithPaginationMeta[type(result)](
            data=result,
            total_entries=count,
            per_page=options.pagination.limit,
            page=options.pagination.page
        )

    async def delete(self, entity: Entity) -> Entity:

        await DomainEvents.publish_events(entity.id, self.__logger)

        await self.__repository.filter(id=entity.id.value).async_delete_with_trigger()

        self.__logger.debug(f'[Entity deleted]: {type(entity).__name__} {entity.id}')

        return entity
        