from uuid import UUID
from core.value_objects.id import ID
from modules.user.database.user.repository import UserRepositoryPort, UserRepository
from modules.user.domain.entities.user import UserEntity, UserProps 
from modules.user.commands.auth.command import CreateUserCommand

from modules.user.database.user_statistic.repository import UserStatisticRepositoryPort, UserStatisticRepository
from modules.user.domain.entities.user_statistic import UserStatisticEntity, UserStatisticProps 

from infrastructure.configs.main import get_mongodb_instance

class UserDService():

    def __init__(self) -> None:
        self.__user_repository: UserRepositoryPort = UserRepository()
        self.__user_statistic_repository: UserStatisticRepositoryPort = UserStatisticRepository()
        self.__db_instance = get_mongodb_instance()

    async def create_user(self, command: CreateUserCommand):
        async with self.__db_instance.session() as session:
             async with session.start_transaction():
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

                    new_user_statistic = UserStatisticEntity(
                        UserStatisticProps(
                            user_id=ID(user.id.value),
                            total_translated_text={},
                            total_translated_doc={}
                        )
                    )
                    await self.__user_statistic_repository.create(new_user_statistic)

                return user

    async def update_user(self, command):
        async with self.__db_instance.session() as session:
            async with session.start_transaction():
                user = await self.__user_repository.find_one({'id': UUID(command.id)})
                if user is None:
                    return None
                changes = dict(command)
                del changes["id"]
                updated_user = await self.__user_repository.update(user, changes)

                return updated_user
    
    async def get_user_statistic(self,user_id):
        async with self.__db_instance.session() as session:
            async with session.start_transaction():
                user = await self.__user_statistic_repository.find_one({'user_id': UUID(user_id)})
                
                if user is None:
                    return None

                return user

    async def update_user_statistic(self,command):
        async with self.__db_instance.session() as session:
            async with session.start_transaction():
                user = await self.__user_statistic_repository.find_one({'user_id': UUID(command.user_id)})
                
                if user is None:
                    return None

                changes = dict(command)

                del changes["user_id"]

                updated_user_statistic = await self.__user_statistic_repository.update(user, changes)

                return updated_user_statistic
