from sanic.views import HTTPMethodView
from sanic_openapi.openapi2 import doc
from sanic import response

import io
from core.utils.audio import get_audio_length
from interface_adapters.dtos.base_response import BaseResponse
from infrastructure.configs.main import GlobalConfig, StatusCodeEnum, get_cnf
from modules.speech_recognition_request.command.create_speech_recognition_request.command import CreateSpeechRecognitionRequestCommand

from infrastructure.configs.message import MESSAGES
from infrastructure.configs.language import LanguageEnum
from infrastructure.configs.speech_recognition_task import is_allowed_file_extension
from core.exceptions.argument_invalid import ArgumentInvalidException
from core.value_objects.id import ID
from core.middlewares.authentication.core import get_me


config: GlobalConfig = get_cnf()
APP_CONFIG = config.APP_CONFIG

class CreateSpeechRecognitionRequest(HTTPMethodView):
    def __init__(self) -> None:
        super().__init__()
        from modules.speech_recognition_request.command.create_speech_recognition_request.service import CreateSpeechRecognitionRequestService

        from modules.user.commands.update_user_statistic.service import UpdateUserStatisticService
        self.__create_speech_recognition_request_service = CreateSpeechRecognitionRequestService()
        self.__update_user_statistic = UpdateUserStatisticService()

    @doc.summary(APP_CONFIG.ROUTES['speech_recognition_request.create']['summary'])
    @doc.description(APP_CONFIG.ROUTES['speech_recognition_request.create']['desc'])
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
        
        user = await get_me(request)
        file = request.files.get("file")
        data = request.form

        if not is_allowed_file_extension(file.name):
            return ArgumentInvalidException(
                message=MESSAGES['failed'],
                metadata=dict(
                    code=StatusCodeEnum.failed.value,
                    data={}
                )
            )

        if request.headers.get('Authorization'):        
            translation_response = await self.create_private_speech_recognition_request(file, data, user)
        else:
            translation_response = await self.create_public_speech_recognition_request(file, data)

        return translation_response

    async def create_public_speech_recognition_request(self, file, data):

        command = CreateSpeechRecognitionRequestCommand(
            creator_id=ID(None),
            source_file=file,
            source_lang=data['sourceLang'][0] if 'sourceLang' in data else None,
        )        

        new_task, new_translation_record = await self.__create_speech_recognition_request_service.create_request(command)

        return response.json(BaseResponse(
            code=StatusCodeEnum.success.value,
            data={
                'taskId': new_task.id.value, 
                'taskName': new_task.props.task_name,
                'translationHitoryId': new_translation_record.id.value
            },
            message=MESSAGES['success']
        ).dict())

    async def create_private_speech_recognition_request(self, file, data, user) -> response:
        pair = "{}-{}".format(data['sourceLang'][0], data['targetLang'][0])

        if user is None:
            return response.json(
                status=401,
                body={
                    'code': StatusCodeEnum.failed.value,
                    'message': MESSAGES['unauthorized']
                }
            )   
            
        file_length = get_audio_length(file)
            
        user_statistic_result =  await self.__update_user_statistic.update_audio_translate_statistic(user.id, pair, file_length)

        if user_statistic_result['code'] == StatusCodeEnum.failed.value:
            return response.json(
                    status=400,
                    body={
                        'code': StatusCodeEnum.failed.value,
                        'message': MESSAGES['audio_translate_limit_reached']
                    }
                )
        else:
            command = CreateSpeechRecognitionRequestCommand(
                creator_id=ID(user.id),
                source_file=file,
                source_lang=data['sourceLang'],
            )
            new_task, new_translation_record = await self.__create_speech_recognition_request_service.create_request(command)

            return response.json(BaseResponse(
                code=StatusCodeEnum.success.value,
                data={
                    'taskId': new_task.id.value, 
                    'taskName': new_task.props.task_name,
                    'translationHitoryId': new_translation_record.id.value
                },
                message=MESSAGES['success']
            ).dict())