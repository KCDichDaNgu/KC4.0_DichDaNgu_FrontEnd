from numbers import Complex
from pydantic.main import BaseModel
from core.base_classes.entity import BaseEntityProps
from core.value_objects.id import ID

from abc import ABC, abstractmethod
from typing import Generic, List, Optional, TypeVar, Awaitable, Any, Union, Dict

Entity = TypeVar('Entity')
EntityProps = TypeVar('EntityProps')
T = TypeVar('T')

OrderBy = Dict[str, Union[str, Complex]]

class PaginationMeta(ABC, BaseModel):

    skip: Optional[int]
    limit: Optional[int]
    page: Optional[int]

class FindManyPaginatedParams(ABC, Generic[EntityProps]):

    params: Optional[Dict]
    pagination: Optional[PaginationMeta]
    orderBy: Optional[OrderBy]

class DataWithPaginationMeta(ABC, Generic[T]):

    data: T
    count: Complex
    limit: Optional[int]
    page: Optional[int]
    

class RepositoryPort(
    ABC, 
    Generic[Entity, EntityProps],
):

    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def save(entity: Entity) -> Awaitable[Entity]:
        ...

    @abstractmethod
    def save_multiple(entity: List[Entity]) -> List[Awaitable[Entity]]:
        ...

    @abstractmethod
    def find_one_or_throw(params: Any) -> Awaitable[Entity]:
        ...

    @abstractmethod
    def find_one_by_id_or_throw(id: Union[ID, str]) -> Awaitable[Entity]:
        ...

    @abstractmethod
    def delete(entity: Entity):
        ...

    @abstractmethod
    def find_many(params: Any) -> Awaitable[List[Entity]]:
        ...

    @abstractmethod
    def find_many_paginated(
        options: FindManyPaginatedParams[EntityProps]
    ) -> Awaitable[DataWithPaginationMeta[List[Entity]]]:
        ...
