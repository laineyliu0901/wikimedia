import gzip
import urllib.request
import os


def get_file_from_pattern(folder, file_pattern):
    for file in os.listdir(folder):
        if file.startswith(file_pattern):
            file_name = folder+'/'+file
    return file_name


def check_pattern(folder, file_pattern):
    return sum([file.startswith(file_pattern) for file in os.listdir(folder)])


def move_file(src, dst):
    if os.path.isfile(src):
            os.rename(src, dst)
    return