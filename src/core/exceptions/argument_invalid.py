from pydantic.fields import PrivateAttr
from core.exceptions.base import ExceptionBase
from core.exceptions.type import Exceptions

class ArgumentInvalidException(ExceptionBase):

    __name: str = PrivateAttr(Exceptions.argument_invalid.value)
