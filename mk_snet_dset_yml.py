import sys
from tqdm import tqdm
import cv2
import fp
from futils import file_pathseq, human_sorted
import imagesize
import imutils

img_dir = './snet_data/image'
inp_idx_fpath = None #TODO -> not None case: not implemented 
out_idx_fpath = '190418snet_idx.yml'
label_dirs = ['./snet_data/clean_rbk', './snet_data/clean_wk']
yml_names  = ['rbk.yml', 'wk.yml']

#TODO Fix some data? dev or..

################## Sanity Checks ####################
#########  Is all same size? ##########
all_same = lambda xs: len(set(xs)) == 1
img_dirs = [img_dir] + label_dirs

file_paths = fp.pipe(
    fp.cmap( file_pathseq ),
    fp.clmap( human_sorted ),
)(img_dirs)
assert all_same(fp.map( len,file_paths ))

not_same_idxs = fp.pipe(
    fp.cmap( fp.cmap(imagesize.get) ),
    fp.unzip,
    enumerate,
    fp.partial(tqdm, total=len(file_paths[0])),
    fp.cremove( lambda i_xs: all_same(i_xs[1]) ),
    fp.cmap( fp.tap ),
    fp.clmap( fp.first ),
)(file_paths)

num_errors = 0
idx_nths = enumerate(fp.list_nths(
    not_same_idxs, fp.lunzip(file_paths)
))
for idx,nth in idx_nths:
    num_errors += 1
    print(idx)
    for fpath in nth:
        print(fpath)
if num_errors == 0:
    print('all image,labels are same size each other!')
else:
    sys.exit('%d image has error...' % num_errors)
######################################################

######## Is cleaned? (check color uniqueness) ########
def invalid_color_idxs(imgpaths, colors):
    return fp.pipe(
    # load and get unique colors
        fp.cmap( cv2.imread ),
        fp.cmap( imutils.num_unique_colors ),
        fp.cmap( fp.first ),
    # check that img is consist of desirable colors
        fp.cmap( fp.rpartial(
            imutils.is_consist_of, colors
        )),
        enumerate, 
        fp.partial(tqdm, total=len(imgpaths)),
    # keep errorneous image indexes
        fp.cremove( fp.val_enum ),
        fp.clmap( fp.idx_enum ), # get index
    )(imgpaths)

wrong_rbk_idxes = invalid_color_idxs(
    file_paths[1],
    [[0,0,255], [255,0,0], [0,0,0]]  # r b k
)

num_errors = 0
for nth in fp.list_nths(wrong_rbk_idxes, 
                        fp.lunzip(file_paths)):
    num_errors += 1
    print(fp.pipe(
        cv2.imread, imutils.num_unique_colors
    )(nth[1]))

if num_errors == 0:
    print('all labels are cleaned!')
else:
    sys.exit('%d image has error...' % num_errors)
######################################################
# Or.. Add your propositions..


    #fp.cmap( fp.pipe(imutls.categorize, fp.second) ),
    #fp.cmap( fp.tap ), # just look & feel!
