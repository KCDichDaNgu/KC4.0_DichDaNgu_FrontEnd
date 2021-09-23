from pydantic import BaseModel
from typing import Union

class AuthCommand(BaseModel):
    username: str
    first_name: str
    last_name: str
    email: str
    avatar: str
    role: str
    status: str
    platform: str