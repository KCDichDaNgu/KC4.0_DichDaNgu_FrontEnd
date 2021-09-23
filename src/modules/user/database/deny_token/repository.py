from modules.user.database.deny_token.orm_entity import DenyTokenOrmEntity
from modules.user.database.deny_token.orm_mapper import DenyTokenOrmMapper
from core.ports.repository import RepositoryPort
from modules.user.domain.entities.deny_token import DenyTokenEntity, DenyTokenProps
from infrastructure.database.base_classes.mongodb.orm_repository_base import OrmRepositoryBase
from typing import get_args

class DenyTokenRepositoryPort(RepositoryPort[DenyTokenEntity, DenyTokenProps]):

    pass

class DenyTokenRepository(OrmRepositoryBase[DenyTokenEntity, DenyTokenProps, DenyTokenOrmEntity, DenyTokenOrmMapper], DenyTokenRepositoryPort):
    @property
    def entity_klass(self):
        return get_args(self.__orig_bases__[0])[0]

    @property
    def repository(self):
        return get_args(self.__orig_bases__[0])[2]

    @property
    def mapper(self):
        return get_args(self.__orig_bases__[0])[3]
