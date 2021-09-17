from uuid import UUID
from modules.translation_request.domain.entities.translation_history import TranslationHistoryEntity
from sanic.exceptions import SanicException
from infrastructure.configs.task import TRANSLATION_PUBLIC_TASKS
from infrastructure.configs.message import MESSAGES
from sanic import response
from modules.translation_history.queries.get_single_translation_history.request_dto import GetSingleTranslationHistoryRequestDto
from infrastructure.configs.main import StatusCodeEnum, GlobalConfig, get_cnf

from sanic_openapi import doc
from sanic.views import HTTPMethodView
from modules.translation_history.dtos.translation_history_response import SingleTranslationHistoryResponse

from core.utils.file import get_task_result_full_file_path

from core.exceptions import NotFoundException

config: GlobalConfig = get_cnf()
APP_CONFIG = config.APP_CONFIG

class GetSingleTranslationHistory(HTTPMethodView):

    def __init__(self) -> None:
        super().__init__()

        from modules.translation_request.database.translation_history.repository import TranslationHistoryRepository
        from modules.translation_request.database.translation_request.repository import TranslationRequestRepository

        self.__translation_history_repository = TranslationHistoryRepository()
        self.__translation_request_repository = TranslationRequestRepository()

    @doc.summary(APP_CONFIG.ROUTES['translation_history.get_single']['summary'])
    @doc.description(APP_CONFIG.ROUTES['translation_history.get_single']['desc'])
    @doc.consumes(
        doc.String(
            description='Task Id',
            name='taskId'
        ), 
        location="query"
    )
    @doc.consumes(
        doc.String(
            description='Translation History Id',
            name='translationHistoryId'
        ), 
        location="query"
    )
    @doc.produces(SingleTranslationHistoryResponse)

    async def get(self, request):
        
        task_id = request.args.get('taskId')
        
        translation_history_id = request.args.get('translationHistoryId')

        query = {}
        
        if not task_id is None:
            query['task_id'] = UUID(task_id)

        if not translation_history_id is None:
            query['id'] = UUID(translation_history_id)
            
        translation_history: TranslationHistoryEntity = await self.__translation_history_repository.find_one(query)
        
        if not translation_history:
            raise NotFoundException('Translation not found')
        
        
        task = await self.__translation_request_repository.find_one({'id': UUID(translation_history.props.task_id.value)})

        if task.props.task_name not in TRANSLATION_PUBLIC_TASKS:
            raise SanicException('Server Error')


        return response.json(body={
            'code': StatusCodeEnum.success.value,
            'data': {
                'taskId': task.id.value,
                'translationType': translation_history.props.translation_type,
                'id': translation_history.id.value,
                'status': translation_history.props.status,
                'updatedAt': str(translation_history.updated_at.value),
                'createdAt': str(translation_history.created_at.value),
                'resultUrl': get_task_result_full_file_path(translation_history.props.file_path)
            },
            'message': MESSAGES['success']
        })