from typing import get_args
from core.value_objects.date import DateVO
from core.base_classes.entity import BaseEntityProps
from pydantic.main import BaseModel
from core.base_classes import Entity
from core.value_objects import ID

class DenyTokenProps(BaseModel):
    token: str
    expired_date: str

class DenyTokenEntity(Entity[DenyTokenProps]):

    def __init__(self, props: DenyTokenProps) -> None:
        super().__init__(props)

    @property
    def props_klass(self):
        return get_args(self.__orig_bases__[0])[0]
