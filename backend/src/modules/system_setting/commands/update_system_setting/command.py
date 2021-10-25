from pydantic import BaseModel
from pydantic.types import conint

class UpdateSystemSettingCommand(BaseModel):

    max_user_text_translation_per_day: conint(ge=0)
    max_user_doc_translation_per_day:  conint(ge=0)
    task_expired_duration: conint(ge=0)
