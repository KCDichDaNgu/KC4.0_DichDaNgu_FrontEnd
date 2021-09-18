from core.value_objects.id import ID
from modules.system_setting.domain.entities.system_setting import SystemSettingEntity, SystemSettingProps
from modules.system_setting.commands.update_system_setting.command import UpdateSystemSettingCommand
from infrastructure.configs.main import get_mongodb_instance

class UpdateSystemSettingService():
    def __init__(self) -> None:

        from modules.system_setting.database.repository import SystemSettingRepositoryPort, SystemSettingRepository

        self.__db_instance = get_mongodb_instance()
        self.__system_setting_repository: SystemSettingRepositoryPort = SystemSettingRepository()

    async def update_system_setting(self, command: UpdateSystemSettingCommand):
        async with self.__db_instance.session() as session:
            async with session.start_transaction():
                
                saved_setting = await self.__system_setting_repository.find_one({})

                conditions = dict(
                    max_user_doc_translation_per_day=command.max_user_doc_translation_per_day,
                    max_user_text_translation_per_day=command.max_user_text_translation_per_day,
                    task_expired_duration=command.task_expired_duration
                )
                
                updated_setting = await self.__system_setting_repository.update(saved_setting, conditions)

                return updated_setting
