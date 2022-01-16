from typing import Optional
from pydantic import BaseModel

class CreateUserCommand(BaseModel):

    username: str
    first_name: Optional[str]
    last_name: Optional[str]
    password: str
    email: str
    role: str
    status: str
    audio_translation_quota: dict
    text_translation_quota: dict
