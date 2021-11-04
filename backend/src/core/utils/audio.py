
import ffmpeg
import os
import tempfile
import random
import string

from core.utils.file import extract_file_extension

def get_audio_length(source_file):

    source_file_ext = extract_file_extension(source_file.name)
    random_str = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(10))
    source_file_name = f'temp_file_{random_str}.{source_file_ext}'
    source_file_full_path = f'tmp/{source_file_name}'

    try:
        with open(source_file_full_path, 'wb+') as outp:

            outp.write(source_file.body)

            outp.close()
        
        
    except Exception as e:
        pass

    duration = int(float(ffmpeg.probe(source_file_full_path)['format']['duration']))

    os.remove(source_file_full_path)
    return duration