from abc import ABC, abstractmethod

class SpeechRecognitorPort(ABC):

    @abstractmethod
    def send_request(self):
        ...
    def check_progress(self):
        ...
    def fetch_text_result(self):
        ...    
    def fetch_result(self):
        ...
    
