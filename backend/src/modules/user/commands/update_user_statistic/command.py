from typing import Dict
from pydantic import BaseModel

class UpdateUserStatisticCommand(BaseModel):

    user_id: str
    total_translated_text: Dict
    total_translated_audio: Dict
    text_translation_quota: int
    audio_translation_quota: int
