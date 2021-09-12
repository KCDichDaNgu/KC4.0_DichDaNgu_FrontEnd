from modules.system_setting.database.repository import SystemSettingRepositoryPort
from modules.system_setting.domain.entities.system_setting import SystemSettingEntity, SystemSettingProps
from modules.system_setting.commands.create_system_setting.command import CreateSystemSettingCommand
from modules.system_setting.database.repository import SystemSettingRepository


class CreateSystemSettingService():

    def __init__(self) -> None:

        self.__system_setting_repository: SystemSettingRepositoryPort = SystemSettingRepository()

    async def create_request(self, command: CreateSystemSettingCommand):
        
        new_request = SystemSettingEntity(
            SystemSettingProps(**{
                # 'editor_id': command.editor_id,
                'max_translate_text_per_day': command.max_translate_text_per_day,
                'max_translate_doc_per_day': command.max_translate_doc_per_day,
                'translation_history_expire_duration': command.translation_history_expire_duration
            })
        )

        created = await self.__system_setting_repository.save(new_request)

        return created
