import imp
from infrastructure.configs.translation_request import TASK_RESULT_FOLDER

def load_module(name):
    """Load module using imp.find_module"""
    names = name.split(".")
    path = None
    
    for name in names:
        f, path, info = imp.find_module(name, path)
        path = [path]

    return imp.load_module(name, f, path[0], info)

def get_task_result_full_file_path(file_path: str):

    return f'{TASK_RESULT_FOLDER}/{file_path}'
