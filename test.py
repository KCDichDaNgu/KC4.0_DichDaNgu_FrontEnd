import aiohttp
import asyncio

async def aaa():
    headers = {'Content-Type': 'application/json'}
    timeout = aiohttp.ClientTimeout(total=60)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.post('http://nmtuet.ddns.net:1820/detect_lang', json={"data": 'hello, this is a test'}, headers=headers) as response:
            result = (await response.json())['data']
if __name__ == '__main__':

    asyncio.run(aaa())