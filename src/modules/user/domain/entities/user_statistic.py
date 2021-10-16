from typing import List, get_args
from pydantic import Field
from pydantic.main import BaseModel
from core.base_classes import Entity
from core.value_objects import ID
from infrastructure.configs.main import StatusCodeEnum
from infrastructure.configs.message import MESSAGES
from interface_adapters.dtos.base_response import BaseResponse

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

    def check_if_reach_text_translate_limit(self, pair, limit):

        if self.props.total_translated_text.get(pair) is None:
            return False

        if self.props.total_translated_text.get(pair) > limit:
            return True

        return False

    def increase_total_translated_text(self, pair, limit):

        if self.props.total_translated_text.get(pair) is None:

            self.props.total_translated_text[pair] = 1
        else:

            if self.props.total_translated_text.get(pair) > limit:
                return BaseResponse(**{
                    "code": StatusCodeEnum.failed.value,
                    "message": MESSAGES['translate_limit_reached'],
                    "data": self.props.total_translated_text
                }).dict()            

            self.props.total_translated_text[pair] += 1 

        return BaseResponse(**{
            "code": StatusCodeEnum.success.value,
            "message": MESSAGES['success'],
            "data": self.props.total_translated_text
        }).dict()

    def increase_total_translated_doc(self, pair, limit):

        if self.props.total_translated_doc.get(pair) is None:

            self.props.total_translated_doc[pair] = 1
        else:

            if self.props.total_translated_doc.get(pair) > limit:
                return BaseResponse(**{
                    "code": StatusCodeEnum.failed.value,
                    "message": MESSAGES['translate_limit_reached'],
                    "data": self.props.total_translated_doc
                }).dict()            

            self.props.total_translated_doc[pair] += 1 

        return BaseResponse(**{
            "code": StatusCodeEnum.success.value,
            "message": MESSAGES['success'],
            "data": self.props.total_translated_doc
        }).dict()
