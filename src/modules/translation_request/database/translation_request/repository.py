from modules.translation_request.database.translation_request.orm_mapper import TranslationRequestOrmMapper
from modules.translation_request.database.translation_request.orm_entity import TranslationRequestOrmEntity
from core.ports.repository import RepositoryPort
from modules.translation_request.domain.entities.translation_request import TranslationRequestEntity, TranslationRequestProps
from infrastructure.database.base_classes.orm_repository_base import OrmRepositoryBase

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
