from uuid import UUID
from core.middlewares.authentication.auth_injection_interface import AuthInjectionInterface
from modules.user.database.token.repository import TokenRepository
from modules.user.database.user.repository import UserRepository


class AuthInjection(AuthInjectionInterface):

    def __init__(self) -> None:
        self.__user_repository: UserRepository = UserRepository()
        self.__access_token_repository : TokenRepository = TokenRepository()

    async def get_token(self, token):
        try:
            return await self.__access_token_repository.find_one({'access_token': UUID(token)})   
        except Exception:
            return None

    async def get_user(self, token):
        try:
            token = await self.__access_token_repository.find_one({'access_token': UUID(token)})
            return await self.__user_repository.find_one({'id': UUID(token.props.user_id.value)})
        except Exception:
            return None
        