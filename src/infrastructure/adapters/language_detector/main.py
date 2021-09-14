from infrastructure.configs.main import GlobalConfig, get_cnf

import aiohttp

from core.ports.language_detector import LanguageDetectorPort

class LanguageDetector(LanguageDetectorPort):

    async def detect(self, url, text, session: aiohttp.ClientSession):

        headers = {'Content-Type': 'application/json'}

        session.request('')
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=text, headers=headers) as response:

                return await response.json()
