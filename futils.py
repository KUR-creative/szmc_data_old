import os
import re
from collections import namedtuple

def filename_ext(path):
    name_ext = namedtuple('name_ext','name ext')
    return name_ext( *os.path.splitext(os.path.basename(path)) )

def filename(path):
    return filename_ext(path).name

def extension(path):
    return filename_ext(path).ext

def file_pathseq(root_dirpath):
    ''' generate file path sequence of directory_path ''' 
    it = os.walk(root_dirpath)
    for root,dirs,files in it:
        for path in map(lambda name:os.path.join(root,name),files):
            yield path

def human_sorted(iterable):
    ''' Sorts the given iterable in the way that is expected. '''
    convert = lambda text: int(text) if text.isdigit() else text
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(iterable, key = alphanum_key)
