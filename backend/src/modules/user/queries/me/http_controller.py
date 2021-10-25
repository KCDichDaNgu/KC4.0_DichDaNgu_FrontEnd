from infrastructure.configs.message import MESSAGES
from sanic import response
from infrastructure.configs.main import StatusCodeEnum, GlobalConfig, get_cnf
from core.middlewares.authentication.core import get_me
import json

from sanic_openapi import doc
from sanic.views import HTTPMethodView

config: GlobalConfig = get_cnf()
APP_CONFIG = config.APP_CONFIG

class GetMe(HTTPMethodView):

    def __init__(self) -> None:
        super().__init__()

    @doc.summary(APP_CONFIG.ROUTES['user.me']['summary'])
    @doc.description(APP_CONFIG.ROUTES['user.me']['desc'])
    @doc.consumes(
        doc.String(
            description="Access token",
            name='Authorization'
        ),
        location='header')
    async def get(self, request):
        user = await get_me(request)
        if user is None:
            return response.json(
                status=404,
                body={
                    'code': StatusCodeEnum.failed.value,
                    'message': MESSAGES['failed']
                }
            )
        return response.json(
            body={
                'code': StatusCodeEnum.success.value,
                'data': {
                    'id': user.id,
                    'username': user.username,
                    'firstName': user.first_name,
                    'lastName': user.last_name,
                    'avatar': user.avatar,
                    'email': user.email,
                    'role': user.role,
                    'status': user.status,
                    'createdAt': user.created_at,
                    'updatedAt': user.updated_at
                },
                'message': MESSAGES['success']
            }
        )

