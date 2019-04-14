from PIL import Image
Image.MAX_IMAGE_PIXELS = 1000000000 
#NOTE:prevent DOS attack error raised from PIL
from scipy import ndimage
import imagesize
from tqdm import tqdm
from pymaybe import maybe
import cv2
#import funcy as F

import fp
from cut_methods import crop_coordseq, resize_to_cut
from access_db import DB

def id_paths(db_path):
    with DB(db_path) as db:
        return db.unparted_raw_img_paths()

repeat_each = fp.pipe(
    zip, 
    fp.cmap(fp.tup(fp.repeat)),
    fp.linto(list)
)

N = 0
def hw_for_cutting(img_h,img_w, cut_h,cut_w, min_cut_h,min_cut_w):
    global N
    #print(N, '/', 5277); N += 1
    if img_h < min_cut_h or img_w < min_cut_w:
        return resize_to_cut(img_h,img_w, min_cut_h,min_cut_w)
    return img_h,img_w

def hw2crop_coord_args(h,w, desired_cut_h, desired_cut_w):
    cut_h = h if h < desired_cut_h else desired_cut_h
    cut_w = w if w < desired_cut_w else desired_cut_w
    return h,w,cut_h,cut_w

def resize(img, h, w):
    return cv2.resize(img, (w,h))

def main():
    data = id_paths('szmc.db')
    ids = data['id']; paths = data['file_path']#[:10]
    min_w = 256
    min_h = 256
    cut_w = 900 
    cut_h = 1200

    num_img = len(data['id'])
    resized_hws = fp.pipe( 
        fp.cmap( lambda im:imagesize.get(im) ),
        fp.cmap( lambda wh: (wh[1],wh[0], cut_h,cut_w, min_h,min_w) ),
        fp.partial( tqdm, total=num_img ),
        fp.clmap( fp.tup(hw_for_cutting) ),
    )(paths)
    print(*resized_hws, sep='\n')
    #print(resized_hws)
    print(list(fp.unzip(resized_hws)))

    crop_coords = fp.pipe(
        fp.cmap( lambda hw: (hw[0],hw[1], cut_h,cut_w) ),
        fp.cmap( fp.tup(hw2crop_coord_args) ),
        fp.cmap( fp.tup(crop_coordseq) ),
        fp.linto(list),
    )(resized_hws)
    print(*crop_coords, sep='\n')

    imgseq = fp.map(ndimage.imread, paths)
    resized_hseq,resized_wseq = fp.unzip(resized_hws)
    resized_imgseq = fp.pipe(
        zip,
        fp.cmap(fp.tup(resize)),
    )( imgseq, resized_hseq, resized_wseq )
    
    for im in resized_imgseq:
        h,w = im.shape[:2]
        assert h >= min_h and w >= min_w
        print(im.shape)
    #images = F.map(wrap(cv2.imread, maybe), paths)
    #for im in images:
    #imgs = F.map(lambda im: ndimage.imread(im), paths)
    #for i,img in enumerate(imgs):
    #    print(img.shape,'{}/{}'.format(i,len(paths)))



if __name__ == '__main__':
    main()

        #print(imagesize.get(imgpath))

    #for h,w,c in tqdm(F.map(lambda im: im.shape.or_else([0,0,0]), images)):
    #    h,w,c
# get raw img paths from db
# load from directories
# rgb->bgr
# resize
# flatmap(cut)
