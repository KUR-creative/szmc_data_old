import cv2
import os
import re

def human_sorted(iterable):
    ''' Sorts the given iterable in the way that is expected. '''
    convert = lambda text: int(text) if text.isdigit() else text
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(iterable, key = alphanum_key)

def file_pathseq(root_dir_path):
    ''' generate file_paths of directory_path ''' 
    it = os.walk(root_dir_path)
    for root,dirs,files in it:
        for path in map(lambda name:os.path.join(root,name),files):
            yield path

img_paths = human_sorted(file_pathseq('./image'))
rbk_paths = human_sorted(file_pathseq('./clean_rbk'))
wk_paths  = human_sorted(file_pathseq('./clean_wk'))

for im_path,rbk_path,wk_path in zip(img_paths,rbk_paths,wk_paths):
    print(im_path)
    print(rbk_path)
    print(wk_path)
    im = cv2.imread(im_path)
    rbk= cv2.imread(rbk_path)
    wk = cv2.imread(wk_path)
    cv2.imshow('im', im)
    cv2.imshow('rbk',rbk)
    cv2.imshow('wk', wk)
    cv2.waitKey(0)
