from pydantic.fields import PrivateAttr
from core.exceptions.base import ExceptionBase
from core.exceptions.type import Exceptions

class DomainException(ExceptionBase):

    __name: str = PrivateAttr(Exceptions.domain_exception.value)
