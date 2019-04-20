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

'''
not_same_hw_idxs = fp.pipe(
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
    not_same_hw_idxs, fp.lunzip(file_paths)
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
'''
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

def print_error_labels(label_paths,colors):
    wrong_rbk_idxes = invalid_color_idxs(
        label_paths,colors
    )
    num_errors = 0
    for lpath in fp.list_nths(wrong_rbk_idxes, 
                              label_paths):
        num_errors += 1
        print('error label:', lpath)
        print(fp.pipe(
            cv2.imread, imutils.num_unique_colors
        )(lpath))

    if num_errors == 0:
        print('all labels are cleaned!')
    else:
        sys.exit('%d image has error...' % num_errors)

'''
# check rbk labels
print_error_labels(
    file_paths[1], [[0,0,255], [255,0,0], [0,0,0]]
)                  # r b k

# check wk labels
print_error_labels(
    file_paths[2], [[255,255,255], [0,0,0]]  # w k
)                 
'''
######################################################
# Or.. Add your propositions..

######### sorted by proportion of not black ##########

img2colormap = fp.pipe(
    imutils.num_unique_colors,
    fp.cmap( lambda arr:arr.tolist() ),
    fp.clmap( fp.tree_leaves ),
    lambda xy:   [fp.chunks(3, xy[0]), xy[1]],
    lambda xy: [fp.into(tuple)(xy[0]), xy[1]],
)

img_sizeseq = fp.pipe(
    fp.cmap( imagesize.get  ),
    fp.cmap( fp.tup(fp.mul) ),
    )(file_paths[0]) 

colormaps = fp.pipe(
    fp.cmap( cv2.imread ),
    fp.cmap( img2colormap ),
    fp.cmap( fp.tup(fp.zipdict) ),
)

rb_colormaps = colormaps(file_paths[1]) 
sorted_id_scoreseq = fp.pipe(
    fp.cmap(
        lambda size,cmap: fp.walk_values(lambda v:v / size,cmap) 
    ),
    fp.cmap( fp.rcurry(fp.omit)( [(0,0,0)] )  ),
    fp.cmap( fp.itervalues ),
    fp.cmap( sum ), # calculate score 
    enumerate,      # get id
    fp.cmap( fp.pipe(reversed,tuple) ),
    fp.partial(tqdm, total=len(file_paths[1])),
    sorted,         # sort by score 
)( img_sizeseq, rb_colormaps )

path_scoreseq = fp.map(
    fp.tup( lambda score,i: [file_paths[1][i],score] ),
    sorted_id_scoreseq
)

print('          path                     score')
for path,score in path_scoreseq:
    print(path, '\t', score)

'''
rb_colormaps = colormaps(file_paths[1])
fs = fp.map(lambda size: lambda value: value / size, img_sizeseq)
rb_proportion_map = fp.pipe(
    fp.construct(list),
    fp.czipmap(fp.tup(fp.cwalk_values)),
    fp.cmap( fp.tap ),
    list,
)(fs, rb_colormaps)
'''
######################################################
