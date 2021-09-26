from pydantic import BaseModel

class UserCommand(BaseModel):

    username: str
    first_name: str
    last_name: str
    email: str
    avatar: str
    role: str
    status: str
