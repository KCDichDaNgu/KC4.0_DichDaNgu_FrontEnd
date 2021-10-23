from infrastructure.configs.speech_recognition_history import SpeechRecognitionHistoryTypeEnum
from interface_adapters.dtos.base_response import BaseResponse
from uuid import UUID
from modules.speech_recognition_request.domain.entities.speech_recognition_history import SpeechRecognitionHistoryEntity
from sanic.exceptions import SanicException
from infrastructure.configs.task import LANGUAGE_DETECTION_PUBLIC_TASKS
from infrastructure.configs.message import MESSAGES
from sanic import response
from infrastructure.configs.main import StatusCodeEnum, GlobalConfig, get_cnf

from sanic_openapi import doc
from sanic.views import HTTPMethodView
from modules.speech_recognition_history.dtos.speech_recognition_history_response import SingleSpeechRecognitionHistoryResponse

from core.utils.file import get_full_path

from core.exceptions import NotFoundException

config: GlobalConfig = get_cnf()
APP_CONFIG = config.APP_CONFIG

class GetSingleSpeechRecognitionHistory(HTTPMethodView):

    def __init__(self) -> None:
        super().__init__()

        from modules.speech_recognition_request.database.speech_recognition_history.repository import SpeechRecognitionHistoryRepository
        from modules.speech_recognition_request.database.speech_recognition_request.repository import SpeechRecognitionRequestRepository

        self.__speech_recognition_history_repository = SpeechRecognitionHistoryRepository()
        self.__speech_recognition_request_repository = SpeechRecognitionRequestRepository()

    @doc.summary(APP_CONFIG.ROUTES['speech_recognition_history.get_single']['summary'])
    @doc.description(APP_CONFIG.ROUTES['speech_recognition_history.get_single']['desc'])
    @doc.consumes(
        doc.String(
            description='Task Id',
            name='taskId'
        ), 
        location="query"
    )
    @doc.consumes(
        doc.String(
            description='SpeechRecognition History Id',
            name='speechRecognitionHistoryId'
        ), 
        location="query"
    )
    @doc.produces(SingleSpeechRecognitionHistoryResponse)

    async def get(self, request):
        
        task_id = request.args.get('taskId')
        
        speech_recognition_history_id = request.args.get('speechRecognitionHistoryId')

        query = {}
        
        if not task_id is None:
            query['task_id'] = UUID(task_id)

        if not speech_recognition_history_id is None:
            query['id'] = UUID(speech_recognition_history_id)
            
        speech_recognition_history: SpeechRecognitionHistoryEntity = await self.__speech_recognition_history_repository.find_one(query)
        
        if not speech_recognition_history:
            raise NotFoundException('SpeechRecognition not found')
        
        task = await self.__speech_recognition_request_repository.find_one({'id': UUID(speech_recognition_history.props.task_id.value)})

        if task.props.task_name == SpeechRecognitionHistoryTypeEnum.private_speech_recognition:
            raise SanicException('Server Error')


        return response.json(BaseResponse(**{
            'code': StatusCodeEnum.success.value,
            'data': {
                'taskId': task.id.value,
                'speechRecognitionType': speech_recognition_history.props.speech_recognition_type,
                'id': speech_recognition_history.id.value,
                'status': speech_recognition_history.props.status,
                'updatedAt': str(speech_recognition_history.updated_at.value),
                'createdAt': str(speech_recognition_history.created_at.value),
                'resultUrl': speech_recognition_history.props.real_file_path
            },
            'message': MESSAGES['success']
        }).dict())
