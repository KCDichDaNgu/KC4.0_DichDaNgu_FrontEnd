from sanic.views import HTTPMethodView
from sanic_openapi.openapi2 import doc
from sanic import response

import io
from interface_adapters.dtos.base_response import BaseResponse
from infrastructure.configs.main import GlobalConfig, StatusCodeEnum, get_cnf

from modules.translation_request.commands.create_file_translation_request.command import CreateFileTranslationRequestCommand

from infrastructure.configs.message import MESSAGES
from infrastructure.configs.language import LanguageEnum
from infrastructure.configs.translation_task import is_allowed_file_extension
from src.core.exceptions.argument_invalid import ArgumentInvalidException


config: GlobalConfig = get_cnf()
APP_CONFIG = config.APP_CONFIG

class CreateFileTranslationRequest(HTTPMethodView):
    def __init__(self) -> None:
        super().__init__()

        from modules.translation_request.commands.create_file_translation_request.service import CreateFileTranslationRequestService
        
        self.__create_file_translation_request_service = CreateFileTranslationRequestService()

    @doc.summary(APP_CONFIG.ROUTES['translation_request.doc_translation.create']['summary'])
    @doc.description(APP_CONFIG.ROUTES['translation_request.doc_translation.create']['desc'])
    @doc.consumes(
        doc.String(
            name="sourceLang",
            description='Source text language',
            required=False,
            choices=LanguageEnum.enum_values()
        ),
        location="formData"
    )
    @doc.consumes(
        doc.String(
            name="targetLang",
            description='Translated text language',
            required=True,
            choices=LanguageEnum.enum_values()
        ),
        location="formData"
    )
    @doc.consumes(
        doc.File(name="file"), 
        location="formData", 
        content_type="multipart/form-data",
    )
    @doc.consumes(
        doc.String(
            description="Access token",
            name='Authorization'
        ),
        location='header'
    )

    async def post(self, request):

        file = request.files.get("file")
        data = request.form
        
        if is_allowed_file_extension(file.name):
            return ArgumentInvalidException(
                message=MESSAGES['failed'],
                metadata=dict(
                    code=StatusCodeEnum.failed.value,
                    data={}
                )
            )
        
        command = CreateFileTranslationRequestCommand(
            source_file=file,
            source_lang=data['sourceLang'][0] if 'sourceLang' in data else None,
            target_lang=data['targetLang'][0]
        )
        
        new_task, new_translation_record = await self.__create_file_translation_request_service.create_request(command)
       
        return response.json(BaseResponse(
            code=StatusCodeEnum.succes.value,
            data={
                'taskId': new_task.id.value, 
                'taskName': new_task.props.task_name,
                'translationHitoryId': new_translation_record.id.value
            },
            message=MESSAGES['success']
        ).dict())
