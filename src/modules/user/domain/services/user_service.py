from core.value_objects.id import ID
from modules.user.database.user.repository import UserRepositoryPort, UserRepository
from modules.user.domain.entities.user import UserEntity, UserProps 
from modules.user.commands.auth.command import UserCommand

from modules.user.database.user_statistic.repository import UserStatisticRepositoryPort, UserStatisticRepository
from modules.user.domain.entities.user_statistic import UserStatisticEntity, UserStatisticProps 

from infrastructure.configs.main import get_mongodb_instance

class UserDService():

    def __init__(self) -> None:
        self.__user_repository: UserRepositoryPort = UserRepository()
        self.__user_statistic_repository: UserStatisticRepositoryPort = UserStatisticRepository()
        self.__db_instance = get_mongodb_instance()

    async def create_user(self, command: UserCommand):
        user = await self.__user_repository.find_one({'email': command.email})
        if user is None:
            async with self.__db_instance.session() as session:
                async with session.start_transaction():
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
                    user_statistic = await self.__user_statistic_repository.create(new_user_statistic)
                    print(user_statistic)

                    return user

