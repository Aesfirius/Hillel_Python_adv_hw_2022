import os
import subprocess
from info_path_sys import path_to_project


def convert_to_mp4(file_name, file_id):
    src = os.path.join(path_to_project, 'src')
    dst = os.path.join(path_to_project, 'new')

    print('[INFO] 1', file_name)
    try:
        _format = ''
        if ".flv" in file_name.lower():
            _format = ".flv"
        if ".mp4" in file_name.lower():
            _format = ".mp4"
        if ".avi" in file_name.lower():
            _format = ".avi"
        if ".mov" in file_name.lower():
            _format = ".mov"
        file_id__file_name = "%s__%s" % (file_id, file_name.lower())
        input_file = os.path.join(src, file_id__file_name)
        print('[INFO] 1', input_file)
        output_file = os.path.join(dst, file_id__file_name.replace(_format, ".mp4"))
        subprocess.Popen(['ffmpeg', '-i', input_file, output_file])
        return output_file
    except Exception as e:
        print(e)
