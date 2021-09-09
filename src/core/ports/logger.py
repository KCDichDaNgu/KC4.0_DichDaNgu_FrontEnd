from abc import ABC, abstractmethod
from typing import Optional, Any

class Logger(ABC):

    @abstractmethod
    def log(message: str, *args, **kwargs):
        ...
    
    @abstractmethod
    def error(message: str, trace: Optional[Any], *args, **kwargs):
        ...
    
    @abstractmethod
    def warn(message: str, *args, **kwargs):
        ...

    @abstractmethod
    def debug(message: str, *args, **kwargs):
        ...
