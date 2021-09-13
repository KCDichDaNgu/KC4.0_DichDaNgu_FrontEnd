from infrastructure.configs.message import MESSAGES
from modules.translation_request.commands.create_plain_text_translation_request.command import CreatePlainTextTranslationRequestCommand
from modules.translation_request.commands.create_plain_text_translation_request.service import CreatePlainTextTranslationRequestService
from sanic import response
from modules.translation_request.commands.create_plain_text_translation_request.request_dto import CreatePlainTextTranslationRequestDto
from infrastructure.configs.main import StatusCodeEnum, GlobalConfig, get_cnf

from sanic_openapi import doc
from sanic.views import HTTPMethodView
from modules.translation_request.dtos.plain_text_translation_response import PlainTextTranslationRequestResponse

config: GlobalConfig = get_cnf()
APP_CONFIG = config.APP_CONFIG

class Body:
    data = doc.Object(CreatePlainTextTranslationRequestDto)


class CreatePlainTextTranslationRequest(HTTPMethodView):

    def __init__(self) -> None:
        super().__init__()

        self.__createPlainTextTranslationRequestService = CreatePlainTextTranslationRequestService()

    @doc.summary(APP_CONFIG.ROUTES['translation_request.text_translation.create']['summary'])
    @doc.description(APP_CONFIG.ROUTES['translation_request.text_translation.create']['desc'])
    @doc.consumes(Body, location="body")
    @doc.produces(PlainTextTranslationRequestResponse)

    async def post(self, request):
        
        data = request.json['data']

        command = CreatePlainTextTranslationRequestCommand(
            source_text=data['sourceText'],
            source_lang=data['sourceLang'],
            target_lang=data['targetLang']
        )

        new_task = await self.__createPlainTextTranslationRequestService.create_request(command)

        return response.json(body={
            'code': StatusCodeEnum.success.value,
            'data': {
                'taskId': new_task.id.value
            },
            'message': MESSAGES['success']
        })
