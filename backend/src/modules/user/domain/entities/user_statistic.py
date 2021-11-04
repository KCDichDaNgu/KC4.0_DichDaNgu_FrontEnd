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
    text_translation_quota: int = Field(...)
    audio_translation_quota: int = Field(...)
    total_translated_text: dict = Field(...)
    total_translated_audio: dict = Field(...)

    class Config:
        use_enum_values = True

class UserStatisticEntity(Entity[UserStatisticProps]):

    def __init__(self, props: UserStatisticProps) -> None:
        super().__init__(props)

    @property
    def props_klass(self):
        return get_args(self.__orig_bases__[0])[0]

    def check_if_reach_text_translate_limit(self, pair):

        if self.props.total_translated_text.get(pair) is None:
            return False

        if self.props.total_translated_text.get(pair) > self.props.text_translation_quota:
            return True

        return False

    def increase_total_translated_text(self, pair, text_length):

        if self.props.total_translated_text.get(pair) is None:

            self.props.total_translated_text[pair] = text_length
        else:

            if self.props.total_translated_text.get(pair) + text_length > self.props.text_translation_quota:
                return BaseResponse(**{
                    "code": StatusCodeEnum.failed.value,
                    "message": MESSAGES['text_translate_limit_reached'],
                    "data": self.props.total_translated_text
                }).dict()            

            self.props.total_translated_text[pair] += text_length

        return BaseResponse(**{
            "code": StatusCodeEnum.success.value,
            "message": MESSAGES['success'],
            "data": self.props.total_translated_text
        }).dict()

    def increase_total_translated_audio(self, pair, audio_length):

        if self.props.total_translated_audio.get(pair) is None:

            self.props.total_translated_audio[pair] = audio_length
        else:

            if self.props.total_translated_audio.get(pair) + audio_length > self.props.audio_translation_quota:
                return BaseResponse(**{
                    "code": StatusCodeEnum.failed.value,
                    "message": MESSAGES['audio_translate_limit_reached'],
                    "data": self.props.total_translated_audio
                }).dict()            

            self.props.total_translated_audio[pair] += audio_length

        return BaseResponse(**{
            "code": StatusCodeEnum.success.value,
            "message": MESSAGES['success'],
            "data": self.props.total_translated_audio
        }).dict()
