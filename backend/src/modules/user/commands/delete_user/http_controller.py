from modules.user.commands.delete_user.command import DeleteUserCommand
from infrastructure.configs.user import UserRole
from interface_adapters.base_classes.response import ResponseBase
from sanic.request import Request
from infrastructure.configs.message import MESSAGES

from sanic import response
from infrastructure.configs.main import StatusCodeEnum, GlobalConfig, get_cnf

from sanic_openapi import doc
from sanic.views import HTTPMethodView

from core.middlewares.authentication.core import login_required

config: GlobalConfig = get_cnf()
APP_CONFIG = config.APP_CONFIG

class DeleteOther(HTTPMethodView):

    def __init__(self) -> None:
        super().__init__()
        from modules.user.domain.services.user_service import UserDService
        self.__user_service = UserDService()

    @doc.summary(APP_CONFIG.ROUTES['admin.delete']['summary'])
    @doc.description(APP_CONFIG.ROUTES['admin.delete']['desc'])
    @doc.consumes(
        doc.String(
            description="Access token",
            name='Authorization'
        ),
        location='header')
    @doc.produces(ResponseBase)
    @login_required(roles=[UserRole.admin.value])
    async def delete(self, request: Request):
        try:
            data = request.json

            command = DeleteUserCommand(
                username=data['username']
            )
            user = await self.__user_service.delete_user(command)

            if user is None:
                return response.json(
                    status=400,
                    body={
                        'code': StatusCodeEnum.failed.value,
                        'message': MESSAGES['failed']
                    }
                )
            return response.json(body={
                'code': StatusCodeEnum.success.value,
                'message': MESSAGES['success']
            })

        except Exception as error:
            print(error)
            return response.json(
                status=500,
                body={
                    'code': StatusCodeEnum.failed.value,
                    'message': MESSAGES['failed']
                }
            )
