import imagesize
from tqdm import tqdm
from pymaybe import maybe
import cv2
import funcy as F

from utils import wrap
from cut_methods import crop_coordseq
from access_db import DB

'''
import funcy as F
import cv2
from pymaybe import maybe
import functools

def main():
    with

if __name__ == '__main__':
    main()
'''

with DB('szmc.db') as db:
    data = db.unparted_raw_img_paths()
    ids = data['id']; paths = data['file_path']
    print(ids)
    print(paths)
    #images = F.map(wrap(cv2.imread, maybe), paths)
    #for im in images:
    for imgpath in paths:
        print(imagesize.get(imgpath))
    #for h,w,c in tqdm(F.map(lambda im: im.shape.or_else([0,0,0]), images)):
    #    h,w,c
# get raw img paths from db
# load from directories
# rgb->bgr
# resize
# flatmap(cut)
