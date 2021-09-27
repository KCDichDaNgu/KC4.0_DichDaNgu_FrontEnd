from modules.user.commands.update_other.command import UpdateOtherUserCommand
from modules.user.domain.services.user_service import UserDService


class UserService():

    def __init__(self) -> None:
        self.__userDService = UserDService()

    async def update_user(self, command: UpdateOtherUserCommand):
        return await self.__userDService.update_user(command=command)