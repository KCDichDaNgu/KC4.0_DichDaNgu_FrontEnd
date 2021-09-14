from infrastructure.configs.main import GlobalConfig, get_cnf

import aiohttp

from core.ports.language_detector import LanguageDetectorPort

config: GlobalConfig = get_cnf()

LANGUAGE_DETECTION_API_URL = config.LANGUAGE_DETECTION_API.URL

class LanguageDetector(LanguageDetectorPort):

    async def detect(self, text, session: aiohttp.ClientSession):

        headers = {'Content-Type': 'application/json'}

        session.request('')
        
        async with aiohttp.ClientSession() as session:
            async with session.post(LANGUAGE_DETECTION_API_URL, data=text, headers=headers) as response:

                return await response.json()
