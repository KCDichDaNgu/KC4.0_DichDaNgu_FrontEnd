from typing import List, get_args
from pydantic import Field
from pydantic.main import BaseModel
from core.base_classes import Entity
from core.value_objects import ID

class UserStatisticProps(BaseModel):

    user_id: ID = Field()
    total_translated_text: dict = Field(...)
    total_translated_doc: dict = Field(...)

    class Config:
        use_enum_values = True

class UserStatisticEntity(Entity[UserStatisticProps]):

    def __init__(self, props: UserStatisticProps) -> None:
        super().__init__(props)

    @property
    def props_klass(self):
        return get_args(self.__orig_bases__[0])[0]
