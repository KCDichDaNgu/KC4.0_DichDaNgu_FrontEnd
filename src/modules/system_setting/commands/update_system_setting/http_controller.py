from modules.system_setting.commands.update_system_setting.service import UpdateSystemSettingService
from modules.system_setting.dtos.system_setting_response import SystemSettingResponse
from sanic import response
from modules.system_setting.commands.update_system_setting.command import UpdateSystemSettingCommand
from modules.system_setting.commands.update_system_setting.request_dto import UpdateSystemSettingDto
from infrastructure.configs.message import MESSAGES
from infrastructure.configs.main import StatusCodeEnum, GlobalConfig, get_cnf
from interface_adapters.dtos.base_response import BaseResponse
from sanic_openapi import doc
from sanic.views import HTTPMethodView
import json

config: GlobalConfig = get_cnf()
APP_CONFIG = config.APP_CONFIG

class Body:
    data = doc.Object(UpdateSystemSettingDto)

class UpdateSystemSetting(HTTPMethodView):

    def __init__(self) -> None:
        super().__init__()

        self.__system_setting_service = UpdateSystemSettingService()

    @doc.summary(APP_CONFIG.ROUTES['system_setting.update']['summary'])
    @doc.description(APP_CONFIG.ROUTES['system_setting.update']['desc'])
    @doc.consumes(Body, location="body")
    @doc.produces(SystemSettingResponse)
    async def put(self, request):

        data = request.json['data']

        command = UpdateSystemSettingCommand(
            max_user_text_translation_per_day=data['maxUserTextTranslationPerDay'],
            max_user_doc_translation_per_day=data['maxUserDocTranslationPerDay'],
            task_expired_duration=data['taskExpiredDuration'],
        )

        saved_setting = await self.__system_setting_service.update_system_setting(command)

        return response.json(BaseResponse(**{
            'code': StatusCodeEnum.success.value,
            'data': {
                'maxUserTextTranslationPerDay': saved_setting.props.max_user_text_translation_per_day,
                'maxUserDocTranslationPerDay': saved_setting.props.max_user_doc_translation_per_day,
                'taskExpiredDuration': saved_setting.props.task_expired_duration,
            },
            'message': MESSAGES['success']
        }).dict())
