from pydantic import BaseModel

class CreateUserCommand(BaseModel):

    username: str
    first_name: str
    last_name: str
    password: str
    email: str
    role: str
    status: str
