from modules.user.database.user.repository import UserRepositoryPort, UserRepository
from modules.user.domain.entities.user import UserEntity, UserProps 
from modules.user.commands.auth.command import UserCommand

class UserDService():

    def __init__(self) -> None:
        self.__user_repository: UserRepositoryPort = UserRepository() 

    async def create_user(self, command: UserCommand):
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
        return user

