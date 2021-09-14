from pydantic import Field
from typing import Any, Optional, Union

from pydantic.fields import PrivateAttr
from core.base_classes.entity import Entity
from pydantic.main import BaseModel
from core.value_objects import ID

import aiofiles
import json, os

from infrastructure.configs.translation_history import TranslationHistoryTypeEnum, TranslationHistoryStatus

class TranslationHistoryProps(BaseModel):
    
    creator_id: ID
    task_id: ID = Field(...)
    task_result_id: ID = Field(...)
    translation_type: TranslationHistoryTypeEnum = Field(...)
    status: TranslationHistoryStatus = Field(...)
    file_path: Optional[str]

    class Config:
        use_enum_values = True

class TranslationHistoryEntity(Entity[TranslationHistoryProps]):

    async def save_request_result_to_file(self, file_path):

        self.props.file_path = file_path

    async def read_data_from_file(self):

        if not self.check_if_file_exists():

            raise FileNotFoundError('File not found')

        async with aiofiles.open(self.props.file_path) as f:
            
            data = json.load(f)

            f.close()

            return data

    async def check_if_file_exists(self):

        return os.path.isfile(self.props.file_path)
