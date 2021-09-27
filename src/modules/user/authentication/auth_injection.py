from uuid import UUID
from core.middlewares.authentication.auth_injection_interface import AuthInjectionInterface
from core.middlewares.authentication.user import User
from modules.user.database.token.repository import TokenRepository
from modules.user.database.user.repository import UserRepository


class AuthInjection(AuthInjectionInterface):

    def __init__(self) -> None:
        self.__user_repository: UserRepository = UserRepository()
        self.__access_token_repository : TokenRepository = TokenRepository()

    async def get_token(self, access_token):
        try:
            return await self.__access_token_repository.find_one({'access_token': UUID(access_token)})   
        except Exception:
            return None

    async def delete_token(self, access_token):
        try:
            return await self.__access_token_repository.delete({'access_token': UUID(access_token)})
        except Exception:
            return None

    async def get_user(self, access_token) -> User:
        try:
            token = await self.__access_token_repository.find_one({'access_token': UUID(access_token)})
            user_entity = await self.__user_repository.find_one({'id': UUID(token.props.user_id.value)})
            if user_entity is None:
                return None
            return User(
                id=user_entity.id.value,
                user_name=user_entity.props.username,
                first_name=user_entity.props.first_name,
                last_name=user_entity.props.last_name,
                avatar=user_entity.props.avatar,
                email=user_entity.props.email,
                role=user_entity.props.role,
                status=user_entity.props.status,
                created_at=user_entity.created_at.value,
                updated_at=user_entity.updated_at.value
            )
        except Exception:
            return None
        