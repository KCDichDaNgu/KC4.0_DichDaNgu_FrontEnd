import imp
import os
import pickle
from typing import IO
import aiofiles
from infrastructure.configs.task import TASK_RESULT_FOLDER
import asyncio
from infrastructure.configs.main import GlobalConfig, get_cnf
from infrastructure.configs.translation_task import SOURCE_FILE_FOLDER

config: GlobalConfig = get_cnf()
STATIC_FOLDER = config.APP_CONFIG.STATIC_FOLDER

def load_module(name):
    """Load module using imp.find_module"""
    names = name.split(".")
    path = None
    
    for name in names:
        f, path, info = imp.find_module(name, path)
        path = [path]

    return imp.load_module(name, f, path[0], info)

def get_task_result_full_file_path(file_path: str):

    return f'{STATIC_FOLDER}/{TASK_RESULT_FOLDER}/{file_path}'

def get_source_file_full_file_path(file_path: str):

    return f'{STATIC_FOLDER}/{SOURCE_FILE_FOLDER}/{file_path}'

def pickle_to_file(file_path: str, data: IO):
    
    full_file_path = get_source_file_full_file_path(file_path)

    try:
        with open(full_file_path, 'wb') as outp:
            
            pickle.dump(data, outp, pickle.HIGHEST_PROTOCOL)

    except Exception as e:
        return None
    
    return full_file_path

async def delete_files(invalid_file_paths):

    delete_request = []

    for file_path in invalid_file_paths:

        full_file_path = get_task_result_full_file_path(file_path)

        if os.path.exists(full_file_path):
            delete_request.append(aiofiles.os.remove(full_file_path))
    
    await asyncio.gather(*delete_request)
