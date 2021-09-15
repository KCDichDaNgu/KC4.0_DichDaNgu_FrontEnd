from modules.translation_request.database.translation_request_result.orm_mapper import TranslationRequestResultOrmMapper
from modules.translation_request.database.translation_request_result.orm_entity import TranslationRequestResultOrmEntity
from core.ports.repository import RepositoryPort
from modules.translation_request.domain.entities.translation_request_result import TranslationRequestResultEntity, TranslationRequestResultProps
from infrastructure.database.base_classes.mongodb.orm_repository_base import OrmRepositoryBase

class TranslationRequestResultRepositoryPort(RepositoryPort[TranslationRequestResultEntity, TranslationRequestResultProps]):

    pass

class TranslationRequestResultRepository(
    OrmRepositoryBase[
        TranslationRequestResultEntity, 
        TranslationRequestResultProps, 
        TranslationRequestResultOrmEntity,
        TranslationRequestResultOrmMapper
    ], 
    TranslationRequestResultRepositoryPort
):

    def __init__(self, 
        repository: TranslationRequestResultOrmEntity = TranslationRequestResultOrmEntity,
        mapper: TranslationRequestResultOrmMapper = TranslationRequestResultOrmMapper(),
        table_name: str = TranslationRequestResultOrmEntity.get_table_name()
    ) -> None:

        super().__init__(
            repository=repository, 
            mapper=mapper,
            table_name=table_name
        )
