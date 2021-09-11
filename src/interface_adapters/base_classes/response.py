from typing import Any
from pydantic.fields import Field
from pydantic import BaseModel

from infrastructure.configs import StatusCodeEnum

class ResponseBase(BaseModel):

    code: StatusCodeEnum = Field(...)
    data: Any
    message: str = Field(...)

    class Config:

        use_enum_values = True
