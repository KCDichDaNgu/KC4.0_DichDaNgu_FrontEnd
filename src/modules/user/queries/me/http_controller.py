from infrastructure.configs.message import MESSAGES
from sanic import response
from infrastructure.configs.main import StatusCodeEnum, GlobalConfig, get_cnf
from infrastructure.authentication.core import login_required

from sanic_openapi import doc
from sanic.views import HTTPMethodView

config: GlobalConfig = get_cnf()
APP_CONFIG = config.APP_CONFIG

class GetMe(HTTPMethodView):

    def __init__(self) -> None:
        super().__init__()

    @login_required
    @doc.summary("test")
    @doc.description("test's description")
    async def get(self, request):
        return response.json(body={
            'code': StatusCodeEnum.success.value,
            'data': {
                'result': 'ok'
            },
            'message': MESSAGES['success']
        })
