# src_json structure:
# { 'img_path1':metadata1, 
#   'img_path2':metadata2, 
#   ...
#   'img_pathN':metadataN, }

import json
from random import shuffle
import fp
import sys

src_json_paths = sys.argv[1:-1]
dst_flist_path = sys.argv[-1]

def json_path2dic(path):
    with open(path, encoding='utf-8') as f:
        return json.load(f)

@fp.curry
def write_flist(path, seq):
    with open(path,'w') as f:
        f.writelines(seq)

def inplace_shuffled(li):
    shuffle(li)
    return li

fp.pipe(
    # paths -> dicts
    fp.cmap(json_path2dic),
    fp.tup(fp.merge),
    lambda dic: dic.items(),
    # dicts -> shuffled image_paths
    fp.cmap(lambda path_val: path_val[0]),
    fp.clmap(lambda path: path + '\n'),
    inplace_shuffled,
    # save
    write_flist(dst_flist_path)
)(src_json_paths)

'''
from pprint import pprint
print(type(fp.merge(json_path2dic(sys.argv[1]), json_path2dic(sys.argv[2]))))
'''
