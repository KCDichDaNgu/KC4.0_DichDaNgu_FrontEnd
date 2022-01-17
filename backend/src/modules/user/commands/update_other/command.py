from typing import Optional
from pydantic import BaseModel

class UpdateOtherUserCommand(BaseModel):

    id: str
    username: Optional[str]
    role: Optional[str]
    status: Optional[str]
    email: Optional[str]
    last_name: Optional[str]
    first_name: Optional[str]
    password: Optional[str]
    audio_translation_quota: Optional[dict]
    text_translation_quota: Optional[dict]
