from typing import Dict
from pydantic import BaseModel

class UpdateUserQuotaCommand(BaseModel):

    text_translation_quota: Dict
    audio_translation_quota: Dict
