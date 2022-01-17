from interface_adapters.interfaces.user_request.delete_user import DeleteOtherUser
from sanic_openapi import doc

class DeleteUserRequestDto(DeleteOtherUser):

    username: doc.String(
        description='username of user to delete',
        name='username'
    )
