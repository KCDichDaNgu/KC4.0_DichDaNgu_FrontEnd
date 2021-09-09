from pydantic.fields import PrivateAttr
from core.exceptions.base import ExceptionBase
from core.exceptions.type import Exceptions

class ArgumentOutOfRangeException(ExceptionBase):

    __name: str = PrivateAttr(Exceptions.argument_out_of_range.value)