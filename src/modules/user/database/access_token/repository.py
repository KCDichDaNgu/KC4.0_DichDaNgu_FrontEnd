from modules.user.database.access_token.orm_entity import AccessTokenOrmEntity
from modules.user.database.access_token.orm_mapper import AccessTokenOrmMapper
from core.ports.repository import RepositoryPort
from modules.user.domain.entities.access_token import AccessTokenEntity, AccessTokenProps
from infrastructure.database.base_classes.mongodb.orm_repository_base import OrmRepositoryBase
from typing import get_args

class AccessTokenRepositoryPort(RepositoryPort[AccessTokenEntity, AccessTokenProps]):

    pass

class AccessTokenRepository(OrmRepositoryBase[AccessTokenEntity, AccessTokenProps, AccessTokenOrmEntity, AccessTokenOrmMapper], AccessTokenRepositoryPort):
    @property
    def entity_klass(self):
        return get_args(self.__orig_bases__[0])[0]

    @property
    def repository(self):
        return get_args(self.__orig_bases__[0])[2]

    @property
    def mapper(self):
        return get_args(self.__orig_bases__[0])[3]
