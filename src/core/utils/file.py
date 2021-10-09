import imp
import os
import aiofiles, asyncio

from infrastructure.configs.task import TASK_RESULT_FOLDER
from infrastructure.configs.main import GlobalConfig, get_cnf

config: GlobalConfig = get_cnf()
STATIC_FOLDER = config.APP_CONFIG.STATIC_FOLDER

def get_full_path(path: str):

    return f'{STATIC_FOLDER}/{path}'

def extract_file_extension(file_name: str):

    file_name_els = file_name.split('.')

    if len(file_name_els) < 2: return ''

    return file_name.split('.')[-1]

async def delete_files(invalid_file_paths):

    delete_request = []

    for file_path in invalid_file_paths:

        full_file_path = get_full_path(file_path)

        if os.path.exists(full_file_path):
            delete_request.append(aiofiles.os.remove(full_file_path))
    
    await asyncio.gather(*delete_request)
