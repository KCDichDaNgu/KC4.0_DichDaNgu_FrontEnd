from sanic import response
from modules.user.domain.services.user_service import UserDService
from modules.user.commands.update_user_statistic.command import UpdateUserStatisticCommand
from modules.system_setting.domain.service.system_setting_service import SystemSettingDService
from infrastructure.configs.main import StatusCodeEnum
from infrastructure.configs.message import MESSAGES

class UpdateUserStatisticService():

    def __init__(self) -> None:
        self.__user_domain_service = UserDService()
        self.__system_setting_service = SystemSettingDService()

    async def update(self, command: UpdateUserStatisticCommand):
        return await self.__user_domain_service.update_user_statistic(command)
    
    async def update_plaintext_translate_statistic(self, user_id, pair):

        system_setting = await self.__system_setting_service.get()
        max_user_text_translation_per_day = system_setting.props.max_user_text_translation_per_day
        
        user_statistic = await self.__user_domain_service.get_user_statistic(user_id)

        increase_total_translated_text_result = user_statistic.increase_total_translated_text(pair, max_user_text_translation_per_day)

        if increase_total_translated_text_result['code'] == StatusCodeEnum.failed.value:

            return increase_total_translated_text_result
        else:

            user_statistic_command = UpdateUserStatisticCommand(
                user_id=user_id,
                total_translated_text=increase_total_translated_text_result['data'],
                total_translated_doc=user_statistic.props.total_translated_doc
            )

            user_statistic = await self.__user_domain_service.update_user_statistic(user_statistic_command)

            return increase_total_translated_text_result

    async def update_file_translate_statistic(self, user_id, pair):

        system_setting = await self.__system_setting_service.get()

        max_user_doc_translation_per_day = system_setting.props.max_user_doc_translation_per_day
        
        user_statistic = await self.__user_domain_service.get_user_statistic(user_id)

        increase_total_translated_doc_result = user_statistic.increase_total_translated_doc(pair, max_user_doc_translation_per_day)

        if increase_total_translated_doc_result['code'] == StatusCodeEnum.failed.value:

            return increase_total_translated_doc_result
        else:

            user_statistic_command = UpdateUserStatisticCommand(
                user_id=user_id,
                total_translated_text=increase_total_translated_doc_result['data'],
                total_translated_doc=user_statistic.props.total_translated_doc
            )

            user_statistic = await self.__user_domain_service.update_user_statistic(user_statistic_command)

            return increase_total_translated_doc_result
