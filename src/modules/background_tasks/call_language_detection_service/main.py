from infrastructure.configs.main import GlobalConfig, get_cnf
from infrastructure.adapters.language_detector.main import LanguageDetector

import asyncio

config: GlobalConfig = get_cnf()
language_detection_api_config = config.LANGUAGE_DETECTION_API

ALLOWED_CONCURRENT_REQUEST = language_detection_api_config.ALLOWED_CONCURRENT_REQUEST

async def main():

    pass

