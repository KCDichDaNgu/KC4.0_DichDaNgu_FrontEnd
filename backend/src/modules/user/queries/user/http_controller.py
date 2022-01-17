
from infrastructure.configs.user import UserRole
from infrastructure.configs.message import MESSAGES
from sanic import response
from infrastructure.configs.main import StatusCodeEnum, GlobalConfig, get_cnf
from core.middlewares.authentication.core import get_me, login_required
import json

from sanic_openapi import doc
from sanic.views import HTTPMethodView

config: GlobalConfig = get_cnf()
APP_CONFIG = config.APP_CONFIG

class GetUser(HTTPMethodView):

    def __init__(self) -> None:
        super().__init__()
        from modules.user.domain.services.user_service import UserDService
        self.__user_domain_service = UserDService()

    @doc.summary(APP_CONFIG.ROUTES['user.get']['summary'])
    @doc.description(APP_CONFIG.ROUTES['user.get']['desc'])
    @doc.consumes(
        doc.String(
            description='user id',
            name='id'
        ),
        location="query"
    )
    @doc.consumes(
        doc.String(
            description="Access token",
            name='Authorization'
        ),
        location='header')
    @login_required(roles=[UserRole.admin.value])

    async def get(self, request):
        user_id =request.args.get('id')

        user = await self.__user_domain_service.get_user(user_id)

        if user is None:
            return response.json(
                status=404,
                body={
                    'code': StatusCodeEnum.failed.value,
                    'message': MESSAGES['failed']
                }
            )

        user_statistic = await self.__user_domain_service.get_user_statistic(user.id.value)

        return response.json(
            body={
                'code': StatusCodeEnum.success.value,
                'data': {
                    'id': user.id.value,
                    'username': user.props.username,
                    'password': user.props.password,
                    'firstName': user.props.first_name,
                    'lastName': user.props.last_name,
                    'avatar': user.props.avatar,
                    'email': user.props.email,
                    'role': user.props.role,
                    'status': user.props.status,
                    'totalTranslatedText':user_statistic.props.total_translated_text,
                    'totalTranslatedAudio':user_statistic.props.total_translated_audio,
                    'audioTranslationQuota':user_statistic.props.audio_translation_quota,
                    'textTranslationQuota':user_statistic.props.text_translation_quota,
                    'createdAt': str(user.created_at.value),
                    'updatedAt': str(user.created_at.value)
                },
                'message': MESSAGES['success']
            }
        )

