import json
from random import shuffle
import fp
import sys

src_json = sys.argv[1] # json created from image_cutter #'./190414cropping.json' 
dst_flist= sys.argv[2] # dataset flist file #'HN_190414_valid.flist' 

# src_json structure:
# { 'img_path1':metadata1, 
#   'img_path2':metadata2, 
#   ...
#   'img_pathN':metadataN, }

with open(src_json) as f:
    dic = json.load(f)

with open(dst_flist,'w') as f:
    lines = fp.pipe(
        fp.cmap(lambda tup: tup[0]),
        fp.clmap(lambda s: s + '\n'),
    )(dic.items())

    shuffle(lines)
    f.writelines(lines)
