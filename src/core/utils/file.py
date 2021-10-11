import imp
import io
import os
import aiofiles, asyncio
from docx import Document

from sanic.request import File

from infrastructure.configs.main import GlobalConfig, get_cnf

config: GlobalConfig = get_cnf()
STATIC_FOLDER = config.APP_CONFIG.STATIC_FOLDER

def get_full_path(path: str):

    return f'{STATIC_FOLDER}/{path}'

def extract_file_extension(file_name: str):

    file_name_els = file_name.split('.')

    if len(file_name_els) < 2: return ''

    return file_name.split('.')[-1]

def get_doc_file_meta(doc_file: File):

    binary_doc = io.BytesIO(doc_file.body)

    file_extension = extract_file_extension(doc_file.name)

    doc = Document(binary_doc)

    total_doc_paragraphs = len(doc.paragraphs)

    return binary_doc, file_extension, total_doc_paragraphs


async def delete_files(invalid_file_paths):

    delete_request = []

    for file_path in invalid_file_paths:

        full_file_path = get_full_path(file_path)

        if os.path.exists(full_file_path):
            delete_request.append(aiofiles.os.remove(full_file_path))
    
    await asyncio.gather(*delete_request)
