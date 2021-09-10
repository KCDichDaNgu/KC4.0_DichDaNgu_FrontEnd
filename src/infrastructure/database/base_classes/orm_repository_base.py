from src.infrastructure.database.base_classes.orm_entity_base import OrmEntityBase
from typing import TypeVar
from core.value_objects.id import ID
from core.domain_events import DomainEvents
from core.ports.logger import Logger
from core.ports.repository import FindManyPaginatedParams, RepositoryPort, DataWithPaginationMeta
from core.exceptions import NotFoundException
from orm_mapper_base import OrmMapper
from core.base_classes.entity import BaseEntityProps
from abc import ABC
from typing import Generic, List, TypeVar, Any, Union

import asyncio

Entity = TypeVar('Entity', BaseEntityProps)
EntityProps = TypeVar('EntityProps')
OrmEntity = TypeVar('OrmEntity', OrmEntityBase)

class OrmRepositoryBase(
    Generic[Entity, EntityProps, OrmEntity], 
    RepositoryPort[Entity, EntityProps],
    ABC
):

    def __init__(self) -> None:

        self.__repository: OrmEntityBase = OrmEntity
        self.__mapper: OrmMapper = OrmMapper[Entity, OrmEntity]()
        self.__logger: Logger = Logger()

        self.__relations: List[str] = []

        self.__table_name__ = OrmEntity.__table_name__
        
    async def save(self, entity: Entity):

        orm_entity = self.__mapper.to_domain_entity(entity)
        
        await DomainEvents.publish_events(entity.id, self.__logger)

        result = await self.__repository.create(orm_entity)

        self.__logger.debug(f'[Entity persisted]: {type(entity).__name__} {entity.id}')
        
        return self.__mapper.to_domain_entity(result)

    async def save_multiple(self, entities: List[Entity]):
        
        result = []

        asyncio.gather(*[DomainEvents.publish_events(entity.id, self.logger) for entity in entities])

        for entity in entities:
            orm_entity = self.__mapper.to_orm_entity(entity)
            new_entity = await self.__repository.create(orm_entity)

            result.append(self.__mapper.to_domain_entity(new_entity))

        self.__logger.debug(f'[Multiple entities persisted]: {Entity.__name__} {"".join(list(map(lambda e: e.id, entities)))}')

        return result

    async def find_one(
        self,
        **params: EntityProps,
    ):

        found = await self.__repository.filter(params).first()

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

    async def find_many(self, params: Any):
        
        result = []

        founds = await self.__repository.filter(params)

        for found in founds:
            result.append(self.__mapper.to_domain_entity(found))

        return result  

    async def find_many_paginated(
        self,
        options: FindManyPaginatedParams[EntityProps]
    ):
        
        result = []

        founds = await self.__repository.filter(options.params)
        
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

        await DomainEvents.publish_events(entity.id, self.__logger);

        await self.__repository.objects(id=entity.id).delete()

        self.__logger.debug(f'[Entity deleted]: {type(entity).__name__} {entity.id}')

        return entity
        