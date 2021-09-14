from modules.translation_request.database.translation_history.orm_mapper import TranslationHistoryOrmMapper
from modules.translation_request.database.translation_history.orm_entity import TranslationHistoryOrmEntity
from core.ports.repository import RepositoryPort
from modules.translation_request.domain.entities.translation_history import TranslationHistoryEntity, TranslationHistoryProps
from infrastructure.database.base_classes.orm_repository_base import OrmRepositoryBase

class TranslationHistoryRepositoryPort(RepositoryPort[TranslationHistoryEntity, TranslationHistoryProps]):

    pass

class TranslationHistoryRepository(
    OrmRepositoryBase[
        TranslationHistoryEntity, 
        TranslationHistoryProps, 
        TranslationHistoryOrmEntity,
        TranslationHistoryOrmMapper
    ], 
    TranslationHistoryRepositoryPort
):

    def __init__(self, 
        repository: TranslationHistoryOrmEntity = TranslationHistoryOrmEntity,
        mapper: TranslationHistoryOrmMapper = TranslationHistoryOrmMapper(),
        table_name: str = TranslationHistoryOrmEntity.get_table_name()
    ) -> None:

        super().__init__(
            repository=repository, 
            mapper=mapper,
            table_name=table_name
        )
