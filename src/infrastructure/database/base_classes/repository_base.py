from _typeshed import Self
from typing import TypeVar
from core.value_objects.id import ID
from core.domain_events import DomainEvent
from core.ports.logger import Logger
from core.ports.repository import FindManyPaginatedParams, RepositoryPort, DataWithPaginationMeta
from core.exceptions import NotFoundException
from orm_mapper_base import OrmMapper
from core.base_classes.entity import BaseEntityProps
from abc import ABC, abstractclassmethod
from cassandra.cqlengine.models import Model
from typing import Generic, List, Optional, TypeVar, Awaitable, Any, Union, Dict


Entity = TypeVar('Entity')
EntityProps = TypeVar('EntityProps')
OrmEntity = TypeVar('OrmEntity')

class RepositoryBase(
    Entity(BaseEntityProps), 
    EntityProps, 
    OrmEntity, 
    RepositoryPort(Entity, EntityProps)):

    def __init__(self) -> None:

        self._repository: Model
        self._mapper: OrmMapper(Entity, OrmEntity)
        self._logger: Logger

    async def save(self, entity: Entity) -> Awaitable[Entity]:

        ormEntity = self._mapper.toOrmEntity(entity)
        result = await self._repository.create(ormEntity)
        self._logger.debug(f'[Entity persisted]: {entity}')
        
        return self._mapper.toDomainEntity(result)

    async def save_multiple(self, entities: List[Entity]) -> List[Awaitable[Entity]]:
        
        result = []

        for entity in entities:
            ormEntity = self._mapper.toOrmEntity(entity)
            newEntity = await self._repository.create(ormEntity)
            result.append(self._mapper.toDomainEntity(newEntity))

        self._logger.debug(f'[Multiple entities persisted]: {entities}')

        return result

    async def find_one(
        self,
        params: EntityProps = {},
    ) -> Awaitable[Entity]:

        found = await self._repository.objects.filter(params)
        found = found.first()

        return self._mapper.toDomainEntity(found) if found else None

    async def find_one_or_throw(self, params: any = {}) -> Awaitable[Entity]:
        
        try:
            found = await self.findOne(params)
        
        except NotFoundException:
            print('Not found')

        return found
            

    async def find_one_by_id_or_throw(self, id: Union[ID, str]) -> Awaitable[Entity]:

        try:
            found = await self._repository.objects.filter(id=id)
            found = found.first()

        except NotFoundException:
            print('Not found')

        return self._mapper.toDomainEntity(found)

    async def find_many(self, params: Any) -> Awaitable[List[Entity]]:
        
        result = []

        founds = await self._repository.objects.filter(params)

        for found in founds:
            result.append(self._mapper.toDomainEntity(found))

        return result  

    async def find_many_paginated(
        self,
        options: FindManyPaginatedParams[EntityProps]
    ) -> Awaitable[DataWithPaginationMeta[List[Entity]]]:
        
        result = []

        founds = await self._repository.filter(options.params)
        count = founds.count()
        founds = founds[options.pagination.skip : options.pagination.limit]
        founds = founds.order_by(options.orderBy)

        for found in founds:
            result.append(self._mapper.toDomainEntity(found))

        return DataWithPaginationMeta({
            'data': result,
            'count': count,
            'limit': options.pagination.limit,
            'page': options.pagination.page
        })

    async def delete(self, entity: Entity) -> Entity:

        await self._repository.delete(self._mapper.toOrmEntity(entity))
        self._logger.debug(f'[Entity deleted]: {entity}')

        return entity