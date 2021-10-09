from interface_adapters.dtos.base_response import BaseResponse
from infrastructure.configs.message import MESSAGES
from modules.translation_request.commands.create_plain_text_translation_request.command import CreatePlainTextTranslationRequestCommand

from sanic import response
from modules.translation_request.commands.create_plain_text_translation_request.request_dto import CreatePlainTextTranslationRequestDto
from infrastructure.configs.main import StatusCodeEnum, GlobalConfig, get_cnf

from sanic_openapi import doc
from sanic.views import HTTPMethodView
from modules.translation_request.dtos.plain_text_translation_response import PlainTextTranslationRequestResponse
from core.middlewares.authentication.core import get_me
from modules.user.commands.update_user_statistic.command import UpdateUserStatisticCommand

config: GlobalConfig = get_cnf()
APP_CONFIG = config.APP_CONFIG

class CreatePlainTextTranslationRequest(HTTPMethodView):

    def __init__(self) -> None:
        super().__init__()

        from modules.translation_request.commands.create_plain_text_translation_request.service import CreatePlainTextTranslationRequestService
        from modules.user.queries.get_user_statistic.service import GetUserStatisticService
        from modules.system_setting.domain.service.system_setting_service import SystemSettingDService
        from modules.user.commands.update_user_statistic.service import UpdateUserStatisticService

        self.__create_plain_text_translation_request_service = CreatePlainTextTranslationRequestService()
        self.__update_user_statistic = UpdateUserStatisticService()

    @doc.summary(APP_CONFIG.ROUTES['translation_request.text_translation.create']['summary'])
    @doc.description(APP_CONFIG.ROUTES['translation_request.text_translation.create']['desc'])
    @doc.consumes(CreatePlainTextTranslationRequestDto, location="body", required=True)
    @doc.consumes(
        doc.String(
            description="Access token",
            name='Authorization'
        ),
        location='header'
    )
    @doc.produces(PlainTextTranslationRequestResponse)

    async def post(self, request):

        user = await get_me(request)
        data = request.json 

        if request.headers.get('Authorization'):        
            translation_response = await self.create_private_plain_text_translation_request(data, user)
        else:
            translation_response = await self.create_public_plain_text_translation_request(data)

        return translation_response

    async def create_public_plain_text_translation_request(self, data):

        command = CreatePlainTextTranslationRequestCommand(
            source_text=data['sourceText'],
            source_lang=data['sourceLang'] if 'sourceLang' in data else None,
            target_lang=data['targetLang']
        )        

        new_task, new_translation_record = await self.__create_plain_text_translation_request_service.create_request(command)

        return response.json(BaseResponse(
            code=StatusCodeEnum.success.value,
            data={
                'taskId': new_task.id.value, 
                'taskName': new_task.props.task_name,
                'translationHitoryId': new_translation_record.id.value
            },
            message=MESSAGES['success']
        ).dict())


    async def create_private_plain_text_translation_request(self, data, user) -> response:

        pair = "{}-{}".format(data['sourceLang'], data['targetLang'])
        
        if user is None:
            return response.json(
                status=401,
                body={
                    'code': StatusCodeEnum.failed.value,
                    'message': MESSAGES['unauthorized']
                }
            )   
            
        user_statistic_result =  await self.__update_user_statistic.update_plaintext_translate_statistic(user.id, pair)

        if user_statistic_result['code'] == StatusCodeEnum.failed.value:
            return response.json(
                    status=400,
                    body={
                        'code': StatusCodeEnum.failed.value,
                        'message': MESSAGES['translate_limit_reached']
                    }
                )
        else:

            command = CreatePlainTextTranslationRequestCommand(
                source_text=data['sourceText'],
                source_lang=data['sourceLang'] if 'sourceLang' in data else None,
                target_lang=data['targetLang']
            )

            new_task, new_translation_record = await self.__create_plain_text_translation_request_service.create_request(command)

            return response.json(BaseResponse(
                code=StatusCodeEnum.success.value,
                data={
                    'taskId': new_task.id.value, 
                    'taskName': new_task.props.task_name,
                    'translationHitoryId': new_translation_record.id.value
                },
                message=MESSAGES['success']
            ).dict())