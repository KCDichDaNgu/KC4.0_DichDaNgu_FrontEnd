from time import time
from pydantic import Field
from pydantic.class_validators import root_validator, validator
from typing import Any, Optional, Union

from pydantic.fields import PrivateAttr
from core.base_classes.entity import Entity
from pydantic.main import BaseModel
from core.value_objects import ID

import aiofiles
import json, os

from infrastructure.configs.translation_request import (
    TASK_RESULT_FOLDER, TASK_RESULT_FILE_EXTENSION, get_full_task_result_file_path
)

class TranslationRequestResultProps(BaseModel):
    
    task_id: ID = Field(...)
    step: str = Field(...)
    file_path: Optional[str]

class TranslationRequestResultEntity(Entity[TranslationRequestResultProps]):

    async def save_request_result_to_file(self, content):

        if not self.props.file_path:
            self.props.file_path = get_full_task_result_file_path(
                created_at=int(round(time() * 1000)), 
                task_id=str(self.props.task_id.value),
                file_extension=TASK_RESULT_FILE_EXTENSION
            )

        async with aiofiles.open(f'{TASK_RESULT_FOLDER}/{self.props.file_path}', 'w+') as f:

            if isinstance(content, str):
                await f.write(json.dumps(json.loads(content)))
            else:
                await f.write(content)

            await f.close()

        return self.check_if_file_exists()

    async def read_data_from_file(self):

        if not self.check_if_file_exists():

            raise FileNotFoundError('File not found')

        async with aiofiles.open(f'{TASK_RESULT_FOLDER}/{self.props.file_path}') as f:
            
            data = await f.read()

            return json.loads(data)

    def check_if_file_exists(self):
        
        return os.path.isfile(f'{TASK_RESULT_FOLDER}/{self.props.file_path}')
