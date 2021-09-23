from functools import partial
from infrastructure.configs.main import Oauth2ProviderAPI
from infrastructure.configs.message import MESSAGES
from infrastructure.configs.main import StatusCodeEnum
from sanic.request import Request
from sanic import Sanic, response
import aiohttp

APP_CONFIG = None

def init_auth(app: Sanic, config):
    global APP_CONFIG
    APP_CONFIG = config

def login_required(async_handler=None):
    if async_handler is None:
        return partial(login_required)

    async def wrapped(route, request: Request, **kwargs):
        print("----------------------------------------------------------------------")
        print(route.__class__)
        print(dir(route))
        print("----------------------------------------------------------------------")
        print(request.__class__)
        print(dir(request))
        print("----------------------------------------------------------------------")
        
        return response.json(
            status=403,
            body={
                'code': StatusCodeEnum.failed.value,
                'message': MESSAGES['failed']
            }
        )
        # return await async_handler(route, request, **kwargs)

    return wrapped

def role_required(async_handler=None, roles=None):
    if async_handler is None:
        return partial(role_required, roles)
    
    async def wrapped(route, request: Request, **kwargs):
        pass
    
    return wrapped

def get_access_token(token):
    pass

async def get_user_from_provider(provider = "GOOGLE", **kwargs):
    providerAPI: Oauth2ProviderAPI = getattr(APP_CONFIG.OAUTH2_PROVIDER, provider)
    async with aiohttp.ClientSession() as session:
        async with session.get(providerAPI.URL, params={**kwargs}) as response:
            result = await response.json()
            return result  
