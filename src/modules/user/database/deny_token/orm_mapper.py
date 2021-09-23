from core.value_objects.id import ID
from typing import Any, get_args
from infrastructure.database.base_classes.mongodb.orm_mapper_base import OrmMapperBase

from modules.user.database.deny_token.orm_entity import DenyTokenOrmEntity
from modules.user.domain.entities.deny_token import DenyTokenEntity, DenyTokenProps

class DenyTokenOrmMapper(OrmMapperBase[DenyTokenEntity, DenyTokenOrmEntity]):

    @property
    def entity_klass(self):
        return get_args(self.__orig_bases__[0])[0]

    @property
    def orm_entity_klass(self):
        return get_args(self.__orig_bases__[0])[1]

    def to_orm_props(self, entity: DenyTokenEntity) -> Any:
        
        props = entity.get_props_copy()

        orm_props = {
            'token': props.token,
            'expired_date': props.expired_date,
        }

        return orm_props

    def to_domain_props(self, orm_entity: DenyTokenOrmEntity) -> DenyTokenProps:
        
        props = {
            'token': orm_entity.token,
            'expired_date': orm_entity.expired_date,
        }

        return props