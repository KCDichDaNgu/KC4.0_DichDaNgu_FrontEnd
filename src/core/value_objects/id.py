from core.utils.uuid import is_valid_uuid
from uuid import uuid4
from core.exceptions.argument_invalid import ArgumentInvalidException
from core.base_classes.value_object import (
    DomainPrimitive,
    ValueObject,
    ValueObjectProps
)
from core.utils import is_valid_uuid

class ID(ValueObject[str]):

    def __init__(self, value: str) -> None:
        super().__init__(ValueObjectProps[str](value))

    @property
    def value(self) -> str:
        return self.props.value

    @staticmethod
    def generate():
        return ID(str(uuid4()))

    @classmethod
    def validate(cls, args: DomainPrimitive[str]):
        if not is_valid_uuid(args.value):
            raise ArgumentInvalidException('Incorrect ID format') 