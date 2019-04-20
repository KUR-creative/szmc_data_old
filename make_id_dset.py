import os
import sys
from pathlib import Path, PurePosixPath
import json
import futils
import fp

# Directory containing files with strange names
raw_dir = sys.argv[1] #'./snet_data/clean_rbk/' 
id_path_json = sys.argv[2] #'rbk.json'

srcpaths = fp.pipe(
    futils.file_pathseq,
    futils.human_sorted,
)(raw_dir)

id_srcpaths = enumerate(srcpaths)

# change name
def make_dstpath(id, path_str):
    path = PurePosixPath(path_str)
    return str(
        PurePosixPath(path.parent) / (str(id) + path.suffix)
    )

dstpaths = fp.lmap( fp.tup(make_dstpath), id_srcpaths )
src_dsts = list(zip( srcpaths,dstpaths ))

for src,dst in src_dsts:
    print( '{} -> {}'.format(src,dst) )
    os.rename(src,dst)

ret = Path(id_path_json)
ret.write_text(json.dumps(src_dsts, indent='\t'))
