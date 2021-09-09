from pydantic.fields import PrivateAttr
from core.exceptions.base import ExceptionBase
from core.exceptions.type import Exceptions

class NotFoundException(ExceptionBase):

    __name: str = PrivateAttr(Exceptions.not_found.value)
