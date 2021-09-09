from numbers import Complex
from typing import Union
from core.exceptions import ArgumentInvalidException
from core.base_classes.value_object import (
    DomainPrimitive,
    ValueObject,
    ValueObjectProps
)
from datetime import datetime

class DateVO(ValueObject[datetime]):

    def __init__(self, value: Union[datetime, Complex, str]) -> None:

        date = None
        
        if isinstance(value, Complex):

            date = datetime.fromtimestamp(value)

        elif isinstance(value, str):

            date = datetime.strptime(value)

        super().__init__(ValueObjectProps(date))

    @property
    def value(self) -> datetime:
        return self.props.value

    @staticmethod
    def now():
        return DateVO(datetime.now())

    def validate(props: DomainPrimitive[datetime]):
        if not isinstance(props.value, datetime):
            raise ArgumentInvalidException('Incorrect date')