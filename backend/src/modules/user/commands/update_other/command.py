from pydantic import BaseModel

class UpdateOtherUserCommand(BaseModel):

    id: str
    role: str
    status: str
