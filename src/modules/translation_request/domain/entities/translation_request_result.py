from pydantic import Field
from pydantic.class_validators import root_validator, validator
from typing import Any, Union

from pydantic.fields import PrivateAttr
from core.base_classes.entity import Entity
from pydantic.main import BaseModel
from core.value_objects import ID

class TranslationRequestResultProps(BaseModel):
    
    task_id: ID = Field(...)
    step: str = Field(...)
    file_path: str

class TranslationRequestResultEntity(Entity[TranslationRequestResultProps]):

    pass
