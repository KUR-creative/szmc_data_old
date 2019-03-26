import json
from pprint import pprint
from collections import namedtuple
def filename_ext(path):
    name_ext = namedtuple('name_ext','name ext')
    return name_ext( *os.path.splitext(os.path.basename(path)) )

def filename(path):
    return filename_ext(path).name

def extension(path):
    return filename_ext(path).ext

from funcy import rcompose, mapcat, tap, partial, map, concat, filter
# id files -> ids
import os
def file_paths(root_dir_path):
    ''' generate file_paths of directory_path ''' 
    it = os.walk(root_dir_path)
    for root,dirs,files in it:
        for path in map(lambda name:os.path.join(root,name),files):
            yield path

def fpath2lines(path,encoding='utf8'):
    with open(path,encoding='utf8') as f:
        return f.readlines()

def unique(seq):
    return type(seq)(set(seq))
def main():
    valid_idset = rcompose(
        file_paths,
        partial(map, filename),
        set,
    )
    id_set = valid_idset('./danbooru_raw/')
    is_valid = lambda j: j['id'] in id_set

    load_jsons = rcompose(
        partial(mapcat, fpath2lines),
        partial(map, json.loads),
    )
    jsons2017 = file_paths('./2017')
    jsons2018 = file_paths('./2018')
    json_paths = concat(jsons2017, jsons2018)
    jsons = load_jsons(json_paths)
    valid_jsons = filter(is_valid, jsons)

    jsons_dic = {}
    for a_json in valid_jsons:
        jid = int(a_json['id'])
        jsons_dic[jid] = a_json 

    jsons_name = 'absurdres_mono.json'
    with open(jsons_name, 'w') as f:
        json.dump(jsons_dic,f)

if __name__ == '__main__':
    main()
