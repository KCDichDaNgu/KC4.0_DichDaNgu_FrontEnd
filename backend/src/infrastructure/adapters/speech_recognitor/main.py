import os
from aiohttp.formdata import FormData
from pydantic.main import BaseModel
from core.ports.speech_recognitor import SpeechRecognitorPort
from infrastructure.configs.language import LanguageEnum
from typing import Any
import aiohttp
from infrastructure.configs.main import GlobalConfig, get_cnf
import requests
config: GlobalConfig = get_cnf()

PUBLIC_SPEECH_RECOGNITION_API_CONF = config.PUBLIC_SPEECH_RECOGNITION_API
PUBLIC_SPEECH_RECOGNITION_API_URL = PUBLIC_SPEECH_RECOGNITION_API_CONF.URL


class SendSpeechRecognitionResponse(BaseModel):

    id: str

    class Config:
        use_enum_values = True

class CheckSpeechRecognitionResponse(BaseModel):

    status: str

    class Config:
        use_enum_values = True

class TextResultSpeechRecognitionResponse(BaseModel):

    text: Any

    class Config:
        use_enum_values = True
class ResultSpeechRecognitionResponse(BaseModel):

    result: Any

    class Config:
        use_enum_values = True



class SpeechRecognitor(SpeechRecognitorPort):
    async def send_request(
        self,
        source_file_full_path: str,
        source_lang: str,
        session: aiohttp.ClientSession = None,
        public_request: bool = True,
    ):

        if public_request:
        
            files = {
                'data_file': ('AUDIO', open(source_file_full_path, 'rb')),
                'config': f'{{"type": "transcription","transcription_config": {{"language": {source_lang}}}}}',
            }                    
            payload = {
                'config': (None, '{\n"type": "transcription",\n"transcription_config": {\n"language": "cmn"\n}\n}'),
            }

            if source_lang == 'en':
                payload = {
                'config': (None, '{\n"type": "transcription",\n"transcription_config": {\n"language": "en"\n}\n}'),
            }

            response = requests.post(PUBLIC_SPEECH_RECOGNITION_API_URL, files=files,data=payload)

            result = (response.json())["id"]

            return SendSpeechRecognitionResponse(id=result)
    
    async def check_progress(
        self, 
        job_id: str, 
        session: aiohttp.ClientSession = None,
        public_request: bool = True
    ):

        if public_request:

            if not session:

                async with aiohttp.ClientSession() as session:
                    async with session.get(f'{PUBLIC_SPEECH_RECOGNITION_API_URL}/{job_id}') as response:
                        result = (await response.json())['job']['status']


                        return CheckSpeechRecognitionResponse(status=result)

            else:
                async with session.get(f'{PUBLIC_SPEECH_RECOGNITION_API_URL}/{job_id}') as response:
                    result = (await response.json())['job']['status']

                    return CheckSpeechRecognitionResponse(status=result)

    async def fetch_text_result(
        self, 
        job_id: str, 
        session: aiohttp.ClientSession = None,
        public_request: bool = True
    ):

        if public_request:
            if not session:

                async with aiohttp.ClientSession() as session:
                    async with session.get(f'{PUBLIC_SPEECH_RECOGNITION_API_URL}/{job_id}/transcript?format=txt') as response:
                        
                        text = await response.text()
                        return TextResultSpeechRecognitionResponse(text=text)

            else:
                async with session.get(f'{PUBLIC_SPEECH_RECOGNITION_API_URL}/{job_id}/transcript?format=txt') as response:
                    text = await response.text()
                    return TextResultSpeechRecognitionResponse(text=text)

    async def fetch_result(
        self, 
        job_id: str, 
        session: aiohttp.ClientSession = None,
        public_request: bool = True
    ):

        if public_request:
            if not session:

                async with aiohttp.ClientSession() as session:
                    async with session.get(f'{PUBLIC_SPEECH_RECOGNITION_API_URL}/{job_id}/transcript') as response:
                        result = await response.json()
                        return ResultSpeechRecognitionResponse(result=result['results'])

            else:
                async with session.get(f'{PUBLIC_SPEECH_RECOGNITION_API_URL}/{job_id}/transcript') as response:
                    result = await response.json()
                    return ResultSpeechRecognitionResponse(result=result['results'])
