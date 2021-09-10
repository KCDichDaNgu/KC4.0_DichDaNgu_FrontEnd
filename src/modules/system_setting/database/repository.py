

from src.modules.system_setting.database.entity import SystemSettingEntity
from src.infrastructure.database.base_classes.orm_repository_base import OrmRepositoryBase


class SystemSettingRepository(OrmRepositoryBase):
    def __init__(self, props: SystemSettingEntity) -> None:
        super().__init__(props)
                                                                