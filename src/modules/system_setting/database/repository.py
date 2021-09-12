
from modules.system_setting.database.orm_mapper import SystemSettingOrmMapper
from modules.system_setting.domain.entities.system_setting import SystemSettingEntity, SystemSettingProps
from modules.system_setting.database.orm_entity import SystemSettingOrmEntity
from core.ports.repository import RepositoryPort
from infrastructure.database.base_classes.mongodb.orm_repository_base import OrmRepositoryBase

class SystemSettingRepositoryPort(RepositoryPort[SystemSettingEntity, SystemSettingOrmEntity]):

    pass

class SystemSettingRepository(
    OrmRepositoryBase[
        SystemSettingEntity, 
        SystemSettingProps, 
        SystemSettingOrmEntity,
        SystemSettingOrmMapper
    ],  
    SystemSettingRepositoryPort
):

    def __init__(self, 
        repository: SystemSettingOrmEntity = SystemSettingOrmEntity,
        mapper: SystemSettingOrmMapper = SystemSettingOrmMapper(),
        table_name: str = SystemSettingOrmEntity.get_table_name()
    ) -> None:

        super().__init__(
            repository=repository, 
            mapper=mapper,
            table_name=table_name
        )
