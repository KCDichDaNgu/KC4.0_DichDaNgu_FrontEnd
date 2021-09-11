from src.modules.translation_request.database.translation_request.orm_entity import TranslationRequestOrmEntity
from src.core.ports.repository import RepositoryPort
from src.modules.translation_request.domain.entities.translation_request import TranslationRequestEntity, TranslationRequestProps
from src.infrastructure.database.base_classes.orm_repository_base import OrmRepositoryBase

class TranslationRequestRepositoryPort(RepositoryPort[TranslationRequestEntity, TranslationRequestProps]):

    pass

class TranslationRequestRepository(OrmRepositoryBase[TranslationRequestEntity, TranslationRequestProps, TranslationRequestOrmEntity], TranslationRequestRepositoryPort):

    pass
