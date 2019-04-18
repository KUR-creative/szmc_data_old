import fp
from futils import file_pathseq, human_sorted
import imagesize

img_dir = './snet_data/image'
inp_idx_fpath = None #TODO -> not None case: not implemented
out_idx_fpath = '190418snet_idx.yml'
label_dirs = ['./snet_data/clean_rbk', './snet_data/clean_wk']
yml_names  = ['rbk.yml', 'wk.yml']

# sanity check
img_dirs = [img_dir] + label_dirs

file_paths = fp.pipe(
    fp.cmap( file_pathseq ),
    fp.clmap( human_sorted ),
)(img_dirs)

all_same = lambda xs: len(set(xs)) == 1
not_same_idxs = fp.pipe(
    fp.cmap( fp.cmap(imagesize.get) ),
    fp.unzip,
    enumerate,
    fp.cremove( lambda i_xs: all_same(i_xs[1]) ),
    fp.cmap( fp.tap ),
    fp.clmap( fp.first ),
)(file_paths)

for idx,nth in enumerate(fp.nths(file_paths, not_same_idxs)):
    print(idx)
    for fpath in nth:
        print(fpath)
