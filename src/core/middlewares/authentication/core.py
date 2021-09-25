from functools import partial
from core.middlewares.authentication.auth_injection_interface import AuthInjectionInterface
from sanic.request import Request
from sanic import response
import aiohttp
from datetime import datetime, timedelta

def init_auth(config, injection: AuthInjectionInterface):
    print(config)
    global AUTH_CONFIG
    global auth_injection

    AUTH_CONFIG = config
    auth_injection = injection

def login_required(async_handler=None, roles=['member']):
    if async_handler is None:
        return partial(login_required, roles=roles)

    async def wrapped(route, request: Request, **kwargs):
        access_token = request.headers.get('Authorization')
        failed_response = response.json(
            status=403,
            body={
                'code': 0,
                'message': 'failed'
            }
        )
        
        if access_token is None:
            return failed_response

        token = await auth_injection.get_token(access_token)
        if token is None:
            return failed_response

        if datetime.now() > token.updated_at.value + timedelta(seconds=token.props.access_expires_in):
            return failed_response

        if token.props.revoked:
            await auth_injection.delete_token(access_token)
            return failed_response

        user = await auth_injection.get_user(access_token)
        if user.props.role not in roles:
            return failed_response

        return await async_handler(route, request, **kwargs)

    return wrapped

async def get_user_from_provider(provider = "GOOGLE", **kwargs):
    providerAPI = getattr(AUTH_CONFIG, provider)
    async with aiohttp.ClientSession() as session:
        async with session.get(providerAPI.URL, params={**kwargs}) as response:
            result = await response.json()
            return result  
