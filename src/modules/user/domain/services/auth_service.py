from os import name
from core.value_objects.date import DateVO
from modules.user.database.user.orm_entity import UserOrmEntity
from core.value_objects import ID
from infrastructure.configs.user import UserRole, UserStatus
from infrastructure.configs.main import get_mongodb_instance, get_cnf, GlobalConfig

from modules.user.database.user.repository import UserRepositoryPort, UserRepository
from modules.user.database.token.repository import TokenRepositoryPort, TokenRepository

from modules.user.domain.entities.user import UserEntity, UserProps 
from modules.user.domain.entities.token import TokenEntity, TokenProps

from modules.user.commands.auth.command import AuthCommand
from infrastructure.configs.token import Scope, TokenType, Platform

config: GlobalConfig = get_cnf()
APP_CONFIG = config.APP_CONFIG

class AuthDService():

    def __init__(self) -> None:
        self.__user_repository: UserRepository = UserRepository()
        self.__token_repository : TokenRepository = TokenRepository()
        self.__db_instance = get_mongodb_instance()    

    async def create_token(self, command: AuthCommand):
        user = await self.__user_repository.find_one({'email': command.email})
        if user is None:
            new_user = UserEntity(
                UserProps(
                    username=command.username,
                    first_name=command.first_name,
                    last_name=command.last_name,
                    email=command.email,
                    avatar=command.avatar,
                    role=command.role,
                    status=command.status,
                )
            )
            user = await self.__user_repository.create(new_user)

        token = TokenEntity(
            TokenProps(
                access_token=ID.generate(),
                refresh_token=ID.generate(),
                token_type=TokenType.bearer.value,
                scope=[Scope.profile.value],
                platform=command.platform,
                user_id=ID(user.id.value),
                expires_in=config.TOKEN_TTL,
                revoked=False
            )
        )
        result = await self.__token_repository.create(token)
        return result
