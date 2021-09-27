from pydantic import BaseModel

class UpdateUserCommand(BaseModel):

    id: str
    first_name: str
    last_name: str
    avatar: str
