from pydantic import BaseModel
from interface_adapters.base_classes.response import ResponseBase

class PlainTextTranslationRequestResponse(ResponseBase):

    class DataStructure(BaseModel):

        taskId: str
        taskType: str
    
    data: DataStructure
