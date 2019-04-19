import cv2
import numpy as np
def to_categorical(y, num_classes=None, dtype='float32'):
    """Converts a class vector (integers) to binary class matrix.
    E.g. for use with categorical_crossentropy.
    # Arguments
        y: class vector to be converted into a matrix
            (integers from 0 to num_classes).
        num_classes: total number of classes.
        dtype: The data type expected by the input, as a string
            (`float32`, `float64`, `int32`...)
    # Returns
        A binary matrix representation of the input. The classes axis
        is placed last.
    # Example
    ```python
    # Consider an array of 5 labels out of a set of 3 classes {0, 1, 2}:
    > labels
    array([0, 2, 1, 2, 0])
    # `to_categorical` converts this into a matrix with as many
    # columns as there are classes. The number of rows
    # stays the same.
    > to_categorical(labels)
    array([[ 1.,  0.,  0.],
           [ 0.,  0.,  1.],
           [ 0.,  1.,  0.],
           [ 0.,  0.,  1.],
           [ 1.,  0.,  0.]], dtype=float32)
    ```
    """

    y = np.array(y, dtype='int')
    input_shape = y.shape
    if input_shape and input_shape[-1] == 1 and len(input_shape) > 1:
        input_shape = tuple(input_shape[:-1])
    y = y.ravel()
    if not num_classes:
        num_classes = np.max(y) + 1
    n = y.shape[0]
    categorical = np.zeros((n, num_classes), dtype=dtype)
    categorical[np.arange(n), y] = 1
    output_shape = input_shape + (num_classes,)
    categorical = np.reshape(categorical, output_shape)
    return categorical


def categorize(img):
    ''' 
    displayable label -> categorized label 
                         (num_channels = num_colors in label) 
    '''
    colors = np.unique(img.reshape(-1,img.shape[2]), axis=0)

    h,w,_ = img.shape
    n_classes = colors.shape[0]
    ret_img = np.zeros((h,w,n_classes))

    img_b, img_g, img_r = np.rollaxis(img, axis=-1)
    origin_map = {}
    for i,(b,g,r) in enumerate(colors):
        category = to_categorical(i, n_classes)
        masks = (img_b == b) & (img_g == g) & (img_r == r) # if [0,0,0]
        ret_img[masks] = category
        origin_map[tuple(map(np.asscalar,category))] \
            = [np.asscalar(b), np.asscalar(g), np.asscalar(r)]
    return ret_img, origin_map

def decategorize(categorized, origin_map):
    ''' 
    categorized label -> displayable label 
    '''
    #TODO: Need to vectorize!
    h,w,n_classes = categorized.shape
    n_channels = len(next(iter(origin_map.values())))
    ret_img = np.zeros((h,w,n_channels))
    for c in range(n_classes):
        category = to_categorical(c, n_classes)
        origin = origin_map[tuple(category)]
        for y in range(h):
            for x in range(w):
                if np.alltrue(categorized[y,x] == category):
                    ret_img[y,x] = origin
    return ret_img

def shape3ch(img3ch):
    assert len(img3ch.shape) == 3
    h,w,c = img3ch.shape
    assert c == 3
    return h,w,c

def num_unique_colors(img3ch):
    h,w,c = shape3ch(img3ch)

    uniques,counts = np.unique(
        img3ch.reshape((h*w, c)), # flatten to 2d arr
        axis=0, return_counts=True
    )
    return uniques,counts

def into2ch(img):
    shape = img.shape
    if len(shape) == 3:
        h,w,c = shape3ch(img)
        return img.reshape((h*w, c))# flatten to 2d arr
    elif len(shape) == 2:
        assert shape[-1] == 3 # rgb or bgr
        return img
    else:
        raise ValueError('unexpected shape of img')


def has_color(img, color) -> bool:
    if img.shape == 3:
        h,w,c = shape3ch(img)
        im = img.reshape((h*w, c)),# flatten to 2d arr
    else:
        im = img

    return any(map( lambda v: all(v == color), im ))

def is_consist_of(img, colors) -> bool:
    colorset = lambda image: set(map(tuple,image))
    im = into2ch(img) # [rgb, rgb, rgb, ...] or bgr..
    return colorset(im) <= colorset(colors)


import unittest
class Test(unittest.TestCase):
    def test_is_consist_of(self):
        img = cv2.imread('snet_data/clean_rbk/180909_Soul Eater Not!_Chapter 028 - Raw_019.png')
        print(is_consist_of(
            img, [[0,0,255], [255,0,0], [0,0,0]]
        ))
        print(is_consist_of(
            num_unique_colors(img)[0],
            [[0,0,255], [255,0,0], [0,0,0]]
        ))

if __name__ == '__main__':
    unittest.main()
