from typing import Optional
from pydantic import BaseModel

class DeleteUserCommand(BaseModel):

    username: str