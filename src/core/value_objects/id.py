from uuid import uuid4
from core.exceptions.argument_invalid import ArgumentInvalidException
from core.utils import is_valid_uuid
from core.base_classes.value_object import (
    DomainPrimitive,
    ValueObject,
    ValueObjectProps
)

class ID(ValueObject[str]):

    def __init__(self, value: str) -> None:
        super().__init__(ValueObjectProps[str](value))

    @property
    def value(self) -> str:
        return self.props.value

    @staticmethod
    def generate():
        return ID(str(uuid4()))

    def validate(self, args: DomainPrimitive[str]):
        if not self(args.value):
            raise ArgumentInvalidException('Incorrect ID format') 