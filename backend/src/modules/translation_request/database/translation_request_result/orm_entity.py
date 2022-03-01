from modules.translation_request.domain.entities.translation_request import TranslationRequestEntity
from infrastructure.configs.translation_task import AllowedFileTranslationExtensionEnum
from infrastructure.database.base_classes.mongodb import OrmEntityBase
from infrastructure.configs.main import MongoDBDatabase, GlobalConfig, get_cnf, get_mongodb_instance
from infrastructure.configs.database import validate_orm_class_name
from modules.task.database.task_result.orm_entity import TaskResultOrmEntity
from modules.task.database.task.repository import TaskRepository

import openpyxl

from infrastructure.configs.task import (
    FILE_TRANSLATION_TASKS,
    PLAIN_TEXT_TRANSLATION_TASKS,
)

import aiofiles
import json, os

from docx import Document

from core.utils.file import get_full_path
from umongo import fields, validate
from infrastructure.configs.task import (
    TASK_RESULT_FILE_EXTENSION, get_task_result_file_name, get_task_result_file_path
)
from core.utils.file import get_doc_file_meta, get_presentation_file_meta, get_worksheet_file_meta, get_txt_file_meta

from nltk.tokenize import sent_tokenize

from uuid import UUID

from openpyxl import Workbook
from pptx import Presentation
from docx import Document

import pickle

config: GlobalConfig = get_cnf()
database_config: MongoDBDatabase = config.MONGODB_DATABASE

db_instance = get_mongodb_instance()

@db_instance.register
@validate_orm_class_name
class TranslationRequestResultOrmEntity(TaskResultOrmEntity):
    
    def pre_insert(self):

        super(TranslationRequestResultOrmEntity, self).pre_insert()

    def pre_update(self):

        super(TranslationRequestResultOrmEntity, self).pre_update()
