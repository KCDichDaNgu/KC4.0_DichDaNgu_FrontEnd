from src.core.value_objects.id import ID
from typing import Generic, List, TypeVar

from pydantic.fields import PrivateAttr
from core.domain_events import DomainEvent, DomainEvents
from core.base_classes.entity import Entity

from abc import ABC

EntityProps = TypeVar('EntityProps')

class AggregateRoot(Entity[EntityProps]):

    __domain_events: List[DomainEvent] = PrivateAttr([])

    def __init__(self, props: EntityProps, id: ID, created_at: DateVO, updated_at: DateVO) -> None:
        super().__init__(props, id, created_at, updated_at)
    
    @property
    def domain_events(self) -> List[DomainEvent]:
        return self.__domain_events

    def add_event(self, domain_event: DomainEvent):

        self.__domain_events.append(domain_event)
        DomainEvents.prepare_for_publish(self)

    def create_events(self):

        self.__domain_events = []
