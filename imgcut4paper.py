import cv2
import os
import fp
import imagesize
from pathlib import Path
import futils
import shutil

mask_paths = list(futils.file_pathseq(
    './dset4paper/clean_wk/'
))

img_paths = Path(
    './dataset/uno_train_cleans190415/db_fmd_cleans190414_valid.flist'
).read_text().split()[:len(mask_paths)]
img_paths = futils.human_sorted(img_paths)

#print(mask_paths)
#print('----')
#print(img_paths)

img_hws = fp.lmap(
    fp.pipe( imagesize.get, fp.tup(lambda w,h: (h,w)) ),
    img_paths
)

def tap(im):
    print(im.shape)
    return im

resizedseq = fp.pipe(
    fp.cmap( 
        lambda p,hw:( cv2.imread(p),tuple(reversed(hw)) )
    ),
    fp.cmap( fp.tup(lambda im,wh: cv2.resize(im,wh)) ),
)(mask_paths, img_hws)

mask_dstpathseq = fp.map(
    fp.pipe( 
        '{}.png'.format, 
        lambda p: str(Path('dset4paper') / 'masks' / p)
    ),
    range(len(mask_paths))
)

for mask,dstpath in zip(resizedseq,mask_dstpathseq):
    #print(ma.shape[:2], hw)
    cv2.imwrite(dstpath,mask)
'''
dst_paths = fp.lmap(
    fp.pipe( 
        '{}.png'.format, 
        lambda p: Path('dset4paper') / 'imgs' / p 
    ),
    range(len(img_paths))
)

# make img_paths directories
mkdir = lambda p: os.makedirs(p, exist_ok=True)
fp.pipe(
    fp.cmap( lambda p: p.parent ),
    fp.foreach( mkdir ),
)(dst_paths)

# copy imgs
for src,dst in zip(img_paths,dst_paths):
    shutil.copyfile( src,dst )
'''


#for i,hw in enumerate(img_hws): print(i,hw)
