import imp
import io
import os
import aiofiles, asyncio
from docx import Document
import shutil
from sanic.request import File
from docx import Document
from docx.document import Document as _Document

from infrastructure.configs.main import GlobalConfig, get_cnf
from docx.table import _Cell, Table
from docx.oxml.text.paragraph import CT_P
from docx.oxml.table import CT_Tbl
from docx.text.paragraph import Paragraph

config: GlobalConfig = get_cnf()
STATIC_FOLDER = config.APP_CONFIG.STATIC_FOLDER

def get_full_path(path: str):

    return f'{STATIC_FOLDER}/{path}'

def extract_file_extension(file_name: str):

    file_name_els = file_name.split('.')

    if len(file_name_els) < 2: return ''

    return file_name.split('.')[-1]

def get_doc_paragraphs(parent):
    if isinstance(parent, _Document):
        parent_elm = parent.element.body
        # print(parent_elm.xml)
    elif isinstance(parent, _Cell):
        parent_elm = parent._tc
    else:
        raise ValueError("something's not right")

    for child in parent_elm.iterchildren():
        if isinstance(child, CT_P):
            yield Paragraph(child, parent)
        elif isinstance(child, CT_Tbl):
            
            table = Table(child, parent)

            for row in table.rows:
                for cell in row.cells:
                    for paragraph in cell.paragraphs:
                        yield paragraph

def get_doc_file_meta(doc_file: File):

    binary_doc = io.BytesIO(doc_file.body)

    doc = Document(binary_doc)

    doc_paragraphs = list(get_doc_paragraphs(doc))

    total_doc_paragraphs = len(doc_paragraphs)

    return binary_doc, total_doc_paragraphs

async def delete_files(invalid_file_paths):

    delete_request = []

    for file_path in invalid_file_paths:

        full_file_path = get_full_path(file_path)

        if os.path.exists(full_file_path):
            delete_request.append(aiofiles.os.remove(full_file_path))
    
    await asyncio.gather(*delete_request)

async def delete_folders(invalid_folders):
    for folder in invalid_folders:

        full_file_path = get_full_path(folder)

        if os.path.exists(full_file_path):
            shutil.rmtree(full_file_path)
