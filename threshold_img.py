import os
import numpy as np
from futils import file_pathseq, human_sorted
import fp
import cv2
from pathlib import PurePosixPath
from tqdm import tqdm

def imtap(im, wait=True, title='im'):
    cv2.imshow(title, im)
    if wait:
        cv2.waitKey(0)
    return im

label_dirs = ['./snet_data/label_rbk', './snet_data/label_wk']
#label_dirs = ['./snet_data/clean_rbk', './snet_data/clean_wk']
dst_dirs = ['./snet_data/clean_rbk', './snet_data/clean_wk']

threshold = 127
thresholded_imgseq = fp.pipe(
    fp.cmap( cv2.imread ),
    #fp.cmap( fp.partial(imtap, wait=False, title='origin') ),
    fp.cmap( lambda im: np.where(im > threshold, 255, 0) ),
    fp.cmap( lambda im: im.astype(np.uint8) ),
)

def dstpathseq(paths, dst_dir):
    return fp.pipe(
        fp.cmap( PurePosixPath ),
        fp.cmap( lambda p: PurePosixPath(dst_dir) / p.name ),
        fp.cmap( lambda p: str(p) ),
    )(paths)
    
for label_dir,dst_dir in zip(label_dirs,dst_dirs):
    os.makedirs(dst_dir, exist_ok=True)
    imgpaths = human_sorted(file_pathseq(label_dir))
    for img,dst in tqdm(zip(thresholded_imgseq(imgpaths),
                            dstpathseq(imgpaths,dst_dir)),
                        total=len(imgpaths)):
        #print(dst)
        #print(img.shape)
        #print(img.dtype)
        cv2.imwrite(dst, img)
