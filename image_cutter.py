from PIL import Image
Image.MAX_IMAGE_PIXELS = 1000000000 
#NOTE:prevent DOS attack error raised from PIL
import imagesize
import imageio
import cv2
import sys

from pathlib import PurePosixPath
from tqdm import tqdm
import json

import fp
from cut_methods import crop_coordseq, resize_to_cut
from access_db import DB

def id_paths(db_path, is_valid=False):
    with DB(db_path) as db:
        if is_valid:
            return db.unparted_raw_img_paths_valid() 
        else:
            return db.unparted_raw_img_paths() # train

repeat_each = fp.pipe(
    zip, 
    fp.cmap(fp.tup(fp.repeat)),
    #fp.linto(list)
)

def cut(img, y0,x0, y1,x1):
    return img[y0:y1, x0:x1]

def hw_for_cutting(img_h,img_w, cut_h,cut_w, min_cut_h,min_cut_w):
    if img_h < min_cut_h or img_w < min_cut_w:
        return resize_to_cut(img_h,img_w, min_cut_h,min_cut_w)
    return img_h,img_w

def hw2crop_coord_args(h,w, desired_cut_h, desired_cut_w):
    cut_h = h if h < desired_cut_h else desired_cut_h
    cut_w = w if w < desired_cut_w else desired_cut_w
    return h,w,cut_h,cut_w

def resize(img, h, w):
    return cv2.resize(img, (w,h))

def dst_path(pathstr, y0,x0, y1,x1):
    path = PurePosixPath(pathstr)
    fname = path.stem + '_{}_{}.png'.format(y0,x0)
    return path.parent / fname

def main():
    json_path = sys.argv[1] #'190414crops_train.json' #'190414crops_valid.json'
    is_valid = (sys.argv[2] == 'valid')
    data = id_paths('szmc.db', is_valid)
    ids = data['id']#[3742:]#[:30]#[523:700] 
    paths = data['file_path']#[3742:]#[:30]#[523:700]
    min_h = 300
    min_w = 300
    cut_h = 1200 #800
    cut_w = 900 

    #print(ids)
    #print(ids[0:1])
    #print(*paths, sep='\n')

    num_img = len(paths)
    resized_hws = fp.pipe( 
        fp.cmap( lambda im:imagesize.get(im) ),
        fp.cmap( lambda wh: (wh[1],wh[0], cut_h,cut_w, min_h,min_w) ),
        fp.partial( tqdm, total=num_img, desc='make resized h,w list' ),
        fp.clmap( fp.tup(hw_for_cutting) ),
    )( paths )
    #print(*resized_hws, sep='\n')

    crop_coords = fp.pipe(
        fp.cmap( lambda hw: (hw[0],hw[1], cut_h,cut_w) ),
        fp.cmap( fp.tup(hw2crop_coord_args) ),
        fp.cmap( fp.tup(crop_coordseq) ),
        fp.linto(list),
    )( resized_hws )
    #print(*crop_coords, sep='\n')

    imgseq = fp.pipe(
        fp.cmap(imageio.imread), 
        fp.partial( tqdm, total=num_img, desc='loading images... ' ),
        #fp.cmap(lambda im: cv2.cvtColor(im, cv2.COLOR_RGB2BGR))
    )(paths)

    resized_imgseq = fp.pipe(
        zip,
        fp.cmap(fp.tup(resize)),
    )( imgseq, *fp.unzip(resized_hws) )
    
    num_crops = fp.lmap(len, crop_coords)
    repeated_pathseq = repeat_each(paths, num_crops)
    repeated_imgseq = repeat_each(resized_imgseq, num_crops)

    y0x0y1x1s = fp.lcat(crop_coords)
    cropseq = fp.pipe(
        zip,
        fp.cmap(fp.tup(cut)),
    )( fp.cat(repeated_imgseq), *fp.unzip(y0x0y1x1s) )

    dst_paths = fp.pipe(
        zip,
        fp.cmap(fp.tup(dst_path)),
        #fp.partial( tqdm, total=num_img, desc='make destination paths' ),
        fp.clmap(str),
    )( fp.cat(repeated_pathseq), *fp.unzip(y0x0y1x1s) )

    for img,path in tqdm(zip(cropseq,dst_paths), 
                         total=len(dst_paths), desc='save images'):
        h,w = img.shape[:2]
        assert h >= min_h and w >= min_w
        #print(path, img.shape)
        #cv2.imwrite(path, img)
        imageio.imwrite(path, img)

    dic = fp.zipdict(dst_paths, fp.into(list)(y0x0y1x1s))
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(dic, f)
    

if __name__ == '__main__':
    main()
