from infrastructure.configs.main import GlobalConfig, get_cnf
from uuid import UUID
from infrastructure.database.base_classes.mongodb import OrmMapperBase, OrmEntityBase
import math

from typing import Dict, TypeVar
from core.value_objects.id import ID
from core.domain_events import DomainEvents
from infrastructure.adapters.logger import Logger
from core.ports.repository import Pagination, RepositoryPort, DataWithPagination
from core.exceptions import NotFoundException

from core.base_classes.entity import BaseEntityProps
from abc import ABC, abstractmethod
from typing import Generic, List, TypeVar, Any, Union

config: GlobalConfig = get_cnf()
APP_CONFIG = config.APP_CONFIG

Entity = TypeVar('Entity', bound=BaseEntityProps)
EntityProps = TypeVar('EntityProps')
OrmEntity = TypeVar('OrmEntity', bound=OrmEntityBase)
OrmMapper = TypeVar('OrmMapper', bound=OrmMapperBase)

class OrmRepositoryBase(
    Generic[Entity, EntityProps, OrmEntity, OrmMapper], 
    RepositoryPort[Entity, EntityProps],
    ABC
):

    def __init__(self) -> None:

        super().__init__()
            
        self.__logger: Logger = Logger(__name__)
        self.__mapper_ins = self.mapper()
    
    @property
    @abstractmethod
    def entity_klass(self):
        # return get_args(self.__orig_bases__[0])[0]
        raise NotImplementedError()

    @property
    @abstractmethod
    def repository(self):
        # return get_args(self.__orig_bases__[0])[1]
        raise NotImplementedError()

    @property
    @abstractmethod
    def mapper(self):
        # return get_args(self.__orig_bases__[0])[2]
        raise NotImplementedError()

    @property
    def logger(self):
        return self.__logger

    @property
    def mapper_ins(self):
        return self.__mapper_ins
        
    async def create(self, entity: Entity):
        
        orm_entity = self.mapper_ins.to_orm_entity(entity)
        
        await DomainEvents.publish_events(entity.id, self.__logger)
        
        await orm_entity.commit()

        self.__logger.debug(f'[Entity persisted]: {type(entity).__name__} {entity.id}')
        
        return self.mapper_ins.to_domain_entity(orm_entity)

    async def update(self, entity: Entity, changes: Any, conditions: Dict = {}):
 
        orm_entity = self.mapper_ins.to_orm_entity(entity)
        
        await DomainEvents.publish_events(entity.id, self.__logger)

        orm_entity.is_created = True
        
        orm_entity.update(changes)

        if conditions:
            await orm_entity.commit(conditions=conditions)
        else:
            await orm_entity.commit()
            
        self.__logger.debug(f'[Entity persisted]: {type(entity).__name__} {entity.id}')
        
        return self.mapper_ins.to_domain_entity(orm_entity)


    async def save(self, entity: Entity, update_conditions: Dict = {}):

        orm_entity = self.mapper_ins.to_orm_entity(entity)
        
        await DomainEvents.publish_events(entity.id, self.__logger)
        
        await orm_entity.commit(conditions=update_conditions)

        self.__logger.debug(f'[Entity persisted]: {type(entity).__name__} {entity.id}')
        
        return self.mapper_ins.to_domain_entity(orm_entity)

    async def find_one(
        self,
        params: Any,
    ):
    
        found = await self.repository.find_one(params)
        
        return self.mapper_ins.to_domain_entity(found) if found else None

    async def find_one_or_throw(self, params: Any = {}):
        
        found = None

        try:
            found = await self.find_one(params)
        
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
        
        cursor = self.repository.find(params)

        if skip:
            cursor = cursor.skip(limit)

        if limit:
            cursor = cursor.limit(limit)

        if order_by:
            cursor = cursor.sort(limit)
            
        result = list((await cursor.to_list(length=None))) if not cursor is None else []
        
        result = list(map(lambda found: self.mapper_ins.to_domain_entity(found), result))

        return result  

    async def find_many_paginated(
        self,
        params: Any,
        pagination: Pagination,
        order_by: Any,
    ):
        max_query_size = APP_CONFIG.MAX_QUERY_SIZE
        result = []

        founds = self.repository.find(params)
        total_entries = await self.repository.count_documents(params)

        if pagination['page']:
            founds = founds.skip((pagination['page']-1)*pagination['per_page'])

        if pagination['per_page']:
            founds = founds.limit(min(max_query_size, pagination['per_page']))

        if order_by:
            founds = founds.sort(order_by)

        result = list((await founds.to_list(length=None))) if not founds is None else []

        result = list(
            map(lambda found: self.mapper_ins.to_domain_entity(found), result))

        return DataWithPagination(
            data=result,
            total_entries=total_entries,
            per_page=min(max_query_size, pagination['per_page']),
            page=pagination['page']
        )

    async def delete(self, entity: Any) -> Entity:        

        if not self.verify_entity_and_curr_klass_is_the_same(entity):
            raise Exception(f'Cannot update entity of {entity.__class__}')

        await DomainEvents.publish_events(entity.id.value, self.__logger)

        await self.repository.find(UUID(entity.id.value)).delete()

        self.__logger.debug(f'[Entity deleted]: {entity.id.value}')

        return entity.id.value
        