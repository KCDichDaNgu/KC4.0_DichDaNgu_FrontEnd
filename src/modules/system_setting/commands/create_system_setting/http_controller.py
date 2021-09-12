from modules.system_setting.dtos.system_setting_response import SystemSettingResponse
from sanic import response
from modules.system_setting.commands.create_system_setting.command import CreateSystemSettingCommand
from modules.system_setting.commands.create_system_setting.service import CreateSystemSettingService
from modules.system_setting.commands.create_system_setting.request_dto import CreateSystemSettingDto
from infrastructure.configs.message import MESSAGES
from infrastructure.configs.main import StatusCodeEnum, GlobalConfig, get_cnf

from sanic_openapi import doc
from sanic.views import HTTPMethodView
import json
config: GlobalConfig = get_cnf()
APP_CONFIG = config.APP_CONFIG


class Body:
    data = doc.Object(CreateSystemSettingDto)


class CreateSystemSetting(HTTPMethodView):

    def __init__(self) -> None:
        super().__init__()

        self.__createSystemSettingService = CreateSystemSettingService()

    @doc.summary(APP_CONFIG.ROUTES['system_setting.create']['summary'])
    @doc.description(APP_CONFIG.ROUTES['system_setting.create']['desc'])
    @doc.consumes(Body, location="body")
    @doc.produces(SystemSettingResponse)
    async def post(self, request):

        data = request.json['data']

        command = CreateSystemSettingCommand(
            # editor_id=data['editorId'],
            max_translate_text_per_day=data['maxTranslateTextPerDay'],
            max_translate_doc_per_day=data['maxTranslateDocPerDay'],
            translation_history_expire_duration=data['translationHistoryExpireDuration'],
        )

        new_task = await self.__createSystemSettingService.create_request(command)
        new_task = new_task.to_object()
        return response.json(body={
            'code': StatusCodeEnum.success.value,
            'data': {
                'editorId': new_task['editor_id'],
                'maxTranslateDocPerDay': new_task['max_translate_doc_per_day'],
                'maxTranslateTextPerDay': new_task['max_translate_text_per_day'],
                'translationHistoryExpireDuration': new_task['translation_history_expire_duration'],
            },
            'message': MESSAGES['success']
        })
