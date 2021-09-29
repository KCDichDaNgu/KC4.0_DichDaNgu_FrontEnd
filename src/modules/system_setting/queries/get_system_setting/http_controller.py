from modules.system_setting.dtos.system_setting_response import SystemSettingResponse
from infrastructure.configs.message import MESSAGES
from interface_adapters.dtos.base_response import BaseResponse
from sanic_openapi import doc
from sanic.views import HTTPMethodView
from sanic import response
from infrastructure.configs.main import GlobalConfig, StatusCodeEnum, get_cnf

config: GlobalConfig = get_cnf()
APP_CONFIG = config.APP_CONFIG

class GetSystemSetting(HTTPMethodView):

    def __init__(self) -> None:

        from modules.system_setting.database.repository import SystemSettingRepository, SystemSettingRepositoryPort

        self.__system_setting_repository: SystemSettingRepositoryPort = SystemSettingRepository()

    @doc.summary(APP_CONFIG.ROUTES['system_setting.get']['summary'])
    @doc.description(APP_CONFIG.ROUTES['system_setting.get']['desc'])
    @doc.produces(SystemSettingResponse)
    
    async def get(self, request):
        saved_setting = await self.__system_setting_repository.find_one({})
        
        return response.json(BaseResponse(**{
            'code': StatusCodeEnum.success.value,
            'data': {
                'editorId': saved_setting.props.editor_id.value,
                'maxUserTextTranslationPerDay': saved_setting.props.max_user_text_translation_per_day,
                'maxUserDocTranslationPerDay': saved_setting.props.max_user_doc_translation_per_day,
                'taskExpiredDuration': saved_setting.props.task_expired_duration,
            },
            'message': MESSAGES['success']
        }).dict())
 