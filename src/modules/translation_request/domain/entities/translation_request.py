from typing import Union
from pydantic.fields import Field
from pydantic.main import BaseModel
from core.base_classes.aggregate_root import AggregateRoot
from enum import Enum
from core.value_objects import DateVO, ID


class TaskType(Enum):

    file_translation = 'file_translation'
    text_translation = 'text_translation'
    language_detection = 'language_detection'


class CreatorType(Enum):

    end_user = 'end_user'


class Status(Enum):

    not_yet_processed = 'not_yet_processed'
    in_progress = 'in_progress'
    completed = 'completed'
    cancelled = 'cancelled'


class TranslationStep(Enum):

    detecting_language = 'detecting_language'
    translating_language = 'translating_language'

class DetectionLanguageStep(Enum):

    detecting_language = 'detecting_language'


class TranslationRequestProps(BaseModel):

    creator_id: ID = Field(...)
    task_type: TaskType = Field(...)
    creator_type: CreatorType = Field(...)
    status: Status = Field(...)
    current_step: Union[TranslationStep, DetectionLanguageStep] = Field(...)
    expired_date: DateVO


class TranslationRequest(AggregateRoot[TranslationRequestProps]):

    def __init__(
        self,
        props: TranslationRequestProps,
        id: ID = None,
        created_at: DateVO = None,
        updated_at: DateVO = None
    ) -> None:
        super().__init__(props, id, created_at, updated_at)

    @staticmethod
    def validate(props: TranslationRequestProps):
        pass
