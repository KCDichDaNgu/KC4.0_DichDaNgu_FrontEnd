from core.base_classes.entity import BaseEntityProps
from pydantic.main import BaseModel
from core.base_classes import Entity
from core.value_objects import ID

class TranslationRequestResultProps(BaseModel):
    
    task_id: ID
    step: str
    result_url: str

class TranslationRequestResultEntity(Entity[TranslationRequestResultProps]):

    def __init__(self, props: TranslationRequestResultProps) -> None:
        super().__init__(props)

    class MergedProps(TranslationRequestResultProps, BaseEntityProps):
        pass

    def get_props_copy(self) -> MergedProps:

        props_copy = {
            'id': self.__id,
            'created_at': self.__created_at,
            'updated_at': self.__updated_at,
            **self.props
        }

        return props_copy
