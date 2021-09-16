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

class CreatePlainTextTranslationRequest(HTTPMethodView):

    def __init__(self) -> None:
        super().__init__()

        self.__create_plain_text_translation_request_service = CreatePlainTextTranslationRequestService()

    @doc.summary(APP_CONFIG.ROUTES['translation_request.text_translation.create']['summary'])
    @doc.description(APP_CONFIG.ROUTES['translation_request.text_translation.create']['desc'])
    @doc.consumes(CreatePlainTextTranslationRequestDto, location="body", required=True)
    @doc.produces(PlainTextTranslationRequestResponse)

    async def post(self, request):
        
        data = request.json

        command = CreatePlainTextTranslationRequestCommand(
            source_text=data['sourceText'],
            source_lang=data['sourceLang'] if 'sourceLang' in data else None,
            target_lang=data['targetLang']
        )

        new_task, new_translation_record = await self.__create_plain_text_translation_request_service.create_request(command)

        return response.json(body={
            'code': StatusCodeEnum.success.value,
            'data': {
                'taskId': new_task.id.value,
                'taskName': new_task.props.task_name,
                'translationHitoryId': new_translation_record.id.value
            },
            'message': MESSAGES['success']
        })
