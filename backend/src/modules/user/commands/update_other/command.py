from typing import Optional
from pydantic import BaseModel

class UpdateOtherUserCommand(BaseModel):

    id: str
    role: str
    status: str
    audio_translation_quota: Optional[dict]
    text_translation_quota: Optional[dict]
