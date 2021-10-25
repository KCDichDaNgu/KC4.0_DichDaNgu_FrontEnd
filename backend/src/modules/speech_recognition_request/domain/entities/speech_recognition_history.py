import json
import os
from typing import Optional
from typing import get_args

import aiofiles
from pydantic import Field
from pydantic.main import BaseModel

from core.base_classes.entity import Entity
from core.utils.file import get_full_path
from core.value_objects import ID
from infrastructure.configs.speech_recognition_history import SpeechRecognitionHistoryTypeEnum, \
    SpeechRecognitionHistoryStatus
from infrastructure.configs.task import get_task_result_file_path

class SpeechRecognitionHistoryProps(BaseModel):
    creator_id: ID
    task_id: ID = Field(...)
    speech_recognition_type: SpeechRecognitionHistoryTypeEnum = Field(...)
    status: SpeechRecognitionHistoryStatus = Field(...)
    file_path: Optional[str]

    class Config:
        use_enum_values = True

    @property
    def real_file_path(self):
        return get_full_path(get_task_result_file_path(self.file_path))

class SpeechRecognitionHistoryEntity(Entity[SpeechRecognitionHistoryProps]):

    @property
    def props_klass(self):
        return get_args(self.__orig_bases__[0])[0]

    async def save_result_file_path(self, file_path):
        self.props.file_path = file_path

    async def read_data_from_file(self):
        if not self.check_if_file_exists():
            raise FileNotFoundError('File not found')

        async with aiofiles.open(self.props.file_path) as f:
            data = json.load(f)

            await f.close()

            return data

    async def check_if_file_exists(self):
        return os.path.isfile(self.props.file_path)
