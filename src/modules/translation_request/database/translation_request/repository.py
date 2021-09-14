import os
import json

from core.value_objects.date import DateVO
from core.value_objects.id import ID
from typing import Any

from cassandra.cqlengine.query import BatchQuery
from modules.translation_request.database.translation_request.orm_mapper import TranslationRequestOrmMapper
from modules.translation_request.database.translation_request.orm_entity import TranslationRequestOrmEntity
from modules.translation_request.domain.entities.translation_request_result import TranslationRequestResultProps
from core.ports.repository import RepositoryPort
from modules.translation_request.domain.entities.translation_request import TranslationRequestEntity, TranslationRequestProps
from infrastructure.database.base_classes.orm_repository_base import OrmRepositoryBase, DomainEvents
from infrastructure.configs.language import LanguageEnum
from infrastructure.configs.translation_request import (
    TASK_RESULT_FOLDER, TASK_RESULT_FILE_PATTERN, TASK_RESULT_FILE_EXTENSION
)
from infrastructure.configs.translation_request import TaskTypeEnum
from modules.translation_request.database.translation_request_result.repository import (
    TranslationRequestResultRepository, 
    TranslationRequestResultEntity
)
from cassandra.cqlengine import ValidationError

translationRequestResultRepository = TranslationRequestResultRepository()

TEXT_TRANSLATION_TASKS = [
    TaskTypeEnum.plain_text_translation.value, 
    TaskTypeEnum.public_plain_text_translation
]

class TranslationRequestRepositoryPort(RepositoryPort[TranslationRequestEntity, TranslationRequestProps]):

    pass

class TranslationRequestRepository(
    OrmRepositoryBase[
        TranslationRequestEntity, 
        TranslationRequestProps, 
        TranslationRequestOrmEntity,
        TranslationRequestOrmMapper
    ], 
    TranslationRequestRepositoryPort
):

    def __init__(self, 
        repository: TranslationRequestOrmEntity = TranslationRequestOrmEntity,
        mapper: TranslationRequestOrmMapper = TranslationRequestOrmMapper(),
        table_name: str = TranslationRequestOrmEntity.get_table_name()
    ) -> None:

        super().__init__(
            repository=repository, 
            mapper=mapper,
            table_name=table_name
        )

    @staticmethod
    async def create_text_translation_handler(batch, result, *args, **kwargs):

        request_data = kwargs.get('request_data')

        if not request_data:

            raise ValidationError('Request data is invalid')

        if not request_data['source_text'] or not request_data['source_lang'] or not request_data['target_lang']:

            raise ValidationError('Request data is missing')

        if not request_data['source_lang'] in LanguageEnum.enum_values() or \
            not request_data['target_lang'] in LanguageEnum.enum_values():

            raise ValidationError('Request language is invalid')
        
        file_name = TASK_RESULT_FILE_PATTERN.format(str(result.id), result.current_step)

        task_result_props = TranslationRequestResultProps.construct(
            task_id=ID(str(result.id)),
            step=result.current_step
        )

        new_task_result_entity = TranslationRequestResultEntity(task_result_props)

        await new_task_result_entity.save_request_result_to_file(
            dir_path=TASK_RESULT_FOLDER,
            file_name=file_name, 
            file_extension=TASK_RESULT_FILE_EXTENSION,
            content=request_data
        )

        result_2 = await translationRequestResultRepository.create(
            new_task_result_entity,
            batch,
            batch_end=False
        )
        
        return result_2

    async def create(
        self, 
        entity: TranslationRequestEntity, 
        batch_ins: Any = None, 
        batch_end = True, 
        **extra_data
    ):
    
        orm_entity = self.mapper.to_orm_entity(entity)

        b = batch_ins if batch_ins else BatchQuery()
        
        await DomainEvents.publish_events(entity.id, self.logger)
        
        new_task = await self.repository.async_create_with_trigger(
            **(orm_entity.to_dict()), 
            batch_ins=b, 
            batch_end=False, 
            **extra_data
        )
        
        if new_task.task_type in TEXT_TRANSLATION_TASKS:

            await self.create_text_translation_handler(b, new_task, **extra_data)

        if not batch_ins is None and batch_end:
            b.execute()

        if not batch_ins is None:
            b.execute()

        self.logger.debug(f'[Entity persisted]: {type(entity).__name__} {entity.id}')
        
        return self.mapper.to_domain_entity(new_task)
