from modules.user.commands.auth.command import UserCommand
from modules.user.domain.services.user_service import UserDService


class UserService():

    def __init__(self) -> None:
        self.__userDService = UserDService()

    async def create_user(self, command: UserCommand):
        return await self.__userDService.create_user(command=command)

