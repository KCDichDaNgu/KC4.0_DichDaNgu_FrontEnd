from pydantic import BaseModel

class CreateSystemSettingCommand(BaseModel):
    
    max_translate_text_per_day: str
    max_translate_doc_per_day:  str
    translation_history_expire_duration: int