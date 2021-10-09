from pydantic import Field
from typing import Optional, get_args, IO
from docx import Document

import pickle
import os

from core.base_classes.entity import Entity
from core.value_objects import ID

from modules.task.domain.entities.task_result import TaskResultEntity, TaskResultProps

from infrastructure.configs.translation_task import (
    FILE_TRANSLATION_FOLDER_PATH,
    FILE_TRANSLATION_TASKS,
    AllowedFileTranslationExtension, 
    get_file_translation_source_file_name,
    get_file_translation_file_path
)

from infrastructure.configs.message import MESSAGES
from infrastructure.configs.main import StatusCodeEnum

from interface_adapters.dtos.base_response import BaseResponse

from core.utils.file import get_full_path

class TranslationRequestResultProps(TaskResultProps):
    
    task_id: ID = Field(...)
    step: str = Field(...)
    file_path: Optional[str]

class TranslationRequestResultEntity(
    TaskResultEntity, 
    Entity[TranslationRequestResultProps]
):

    @property
    def props_klass(self):
        return get_args(self.__orig_bases__[1])[0]

    def __create_file_translation_task_folder(self):

        real_file_translation_task_folder = get_full_path(FILE_TRANSLATION_FOLDER_PATH)

        if not os.path.isdir(real_file_translation_task_folder):

            os.makedirs(real_file_translation_task_folder)

        return real_file_translation_task_folder

    async def create_required_files_for_file_translation_task(
        self,
        binary_doc: IO,
        original_file_ext: AllowedFileTranslationExtension
    ):

        if self.props.task_name not in FILE_TRANSLATION_TASKS:
            raise ValueError('Translation task is not file translation')
            
        original_file_name = f'{get_file_translation_source_file_name()}.{original_file_ext}'
        original_file_path = get_file_translation_file_path(self.props.task_id.value, original_file_name)
        original_file_full_path = get_full_path(original_file_path)


        saved_process_file_name = f'{get_file_translation_source_file_name()}.json'
        saved_process_file_path = get_file_translation_file_path(self.props.task_id.value, saved_process_file_name)
        saved_process_file_full_path = get_full_path(saved_process_file_path)

        self.__create_file_translation_task_folder()

        try:

            doc = Document(original_file_full_path)

            doc.save(get_full_path)

            with open(saved_process_file_full_path, 'wb') as outp:
            
                pickle.dump(binary_doc, outp, pickle.HIGHEST_PROTOCOL)

        except Exception as e:

            return BaseResponse(
                code=StatusCodeEnum.failed.value,
                data=dict(
                    original_file_name=None,
                    saved_process_file_path=None
                ),
                messages=str(e)
            )
        
        return BaseResponse(
            code=StatusCodeEnum.failed.value,
            data=dict(
                original_file_path=None,
                saved_process_file_path=None
            ),
            messages=MESSAGES['success']
        )
