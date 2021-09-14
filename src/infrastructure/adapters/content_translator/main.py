from infrastructure.configs.main import GlobalConfig, get_cnf

import aiohttp

from core.ports.content_translator import ContentTranslatorPort

config: GlobalConfig = get_cnf()

TRANSLATION_API_URL = config.TRANSLATION_API.URL

class ContentTranslator(ContentTranslatorPort):

    async def translate(self, source_lang, target_lang, source_text):

        direction = f'{source_lang}-{target_lang}'

        data = {
            'direction': direction,
            'data': source_text
        }

        headers = {'Content-Type': 'application/json'}
        
        async with aiohttp.ClientSession() as session:
            async with session.post(TRANSLATION_API_URL, data=data, headers=headers) as response:

                return await response.json()
