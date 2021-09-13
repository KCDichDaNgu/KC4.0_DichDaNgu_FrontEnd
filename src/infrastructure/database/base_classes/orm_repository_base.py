from infrastructure.database.base_classes.orm_entity_base import OrmEntityBase
from typing import NewType, TypeVar
from core.value_objects.id import ID
from core.domain_events import DomainEvents
from infrastructure.adapters.logger import Logger
from core.ports.repository import FindManyPaginatedParams, RepositoryPort, DataWithPaginationMeta
from core.exceptions import NotFoundException
from infrastructure.database.base_classes.orm_mapper_base import OrmMapperBase
from core.base_classes.entity import BaseEntityProps
from abc import ABC
from typing import Generic, List, TypeVar, Any, Union
from cassandra.cqlengine.query import BatchQuery

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
        
    async def save(self, entity: Entity):
        
        orm_entity = self.__mapper.to_orm_entity(entity)
        
        await DomainEvents.publish_events(entity.id, self.__logger)
        
        result = self.__repository.create(**(orm_entity.to_dict()))

        self.__logger.debug(f'[Entity persisted]: {type(entity).__name__} {entity.id}')
        
        return self.__mapper.to_domain_entity(result)

    async def save_multiple(self, entities: List[Entity]):
        
        result = []

        asyncio.gather(*[DomainEvents.publish_events(entity.id, self.logger) for entity in entities])

        with BatchQuery() as b:
            for entity in entities:

                orm_entity = self.__mapper.to_orm_entity(entity)
                new_entity = self.__repository.batch(b).async_create(**(orm_entity.to_dict()))

                result.append(self.__mapper.to_domain_entity(new_entity))

        self.__logger.debug(f'[Multiple entities persisted]: {Entity.__name__} {"".join(list(map(lambda e: e.id, entities)))}')

        return result

    async def find_one(
        self,
        **params: EntityProps,
    ):

        found = await self.__repository.async_filter(params).first()

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

        founds = await self.__repository.async_filter(params)

        for found in founds:
            result.append(self.__mapper.to_domain_entity(found))

        return result  

    async def find_many_paginated(
        self,
        options: FindManyPaginatedParams[EntityProps]
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

        await DomainEvents.publish_events(entity.id, self.__logger);

        await self.__repository.objects(id=entity.id).delete()

        self.__logger.debug(f'[Entity deleted]: {type(entity).__name__} {entity.id}')

        return entity
        