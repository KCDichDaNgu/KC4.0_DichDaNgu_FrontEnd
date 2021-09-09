from core.base_classes.entity import BaseEntityProps
from interface_adapters.dtos import IdResponse

class ResponseBase(IdResponse):

    created_at: str
    updated_at: str

    def __init__(self, entity: BaseEntityProps) -> None:
        
        super().__init__(str(entity.id.value) if entity.id else str(None))

        self.created_at = str(entity.created_at.value) if entity.created_at else str(None)
        self.updated_at = str(entity.updated_at.value) if entity.updated_at else str(None)

