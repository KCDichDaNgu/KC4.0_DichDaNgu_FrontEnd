from functools import partial
from infrastructure.authentication.auth_injection_interface import AuthInjectionInterface
from infrastructure.configs.main import Oauth2ProviderAPI
from infrastructure.configs.message import MESSAGES
from infrastructure.configs.main import StatusCodeEnum
from sanic.request import Request
from sanic import response
import aiohttp
from datetime import datetime, timedelta

def init_auth(config, injection: AuthInjectionInterface):
    global AUTH_CONFIG
    global auth_injection

    AUTH_CONFIG = config
    auth_injection = injection

def login_required(async_handler=None, roles=['member']):
    if async_handler is None:
        return partial(login_required, roles=roles)

    async def wrapped(route, request: Request, **kwargs):
        token = request.headers.get('Authorization')
        failed_response = response.json(
            status=403,
            body={
                'code': StatusCodeEnum.failed.value,
                'message': MESSAGES['failed']
            }
        )
        
        if token is None:
            return failed_response

        if await auth_injection.get_deny_token(token) is not None:
            return failed_response

        access_token = await auth_injection.get_token(token)
        if access_token is None:
            return failed_response

        if datetime.now() > access_token.created_at.value + timedelta(seconds=access_token.props.expires_in) or access_token.props.revoked:
            return failed_response

        user = await auth_injection.get_user(token)
        print(user.props.role, roles)
        if user.props.role not in roles:
            return failed_response

        return await async_handler(route, request, **kwargs)

    return wrapped

async def get_user_from_provider(provider = "GOOGLE", **kwargs):
    providerAPI: Oauth2ProviderAPI = getattr(AUTH_CONFIG, provider)
    async with aiohttp.ClientSession() as session:
        async with session.get(providerAPI.URL, params={**kwargs}) as response:
            result = await response.json()
            return result  
