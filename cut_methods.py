import funcy as F

def crop_coordseq(img_h,img_w, cut_h,cut_w):
    assert cut_h <= img_h and cut_w <= img_w
    ys = [0] + [i*cut_h for i in range(1,img_h // cut_h)] + [img_h]
    xs = [0] + [i*cut_w for i in range(1,img_w // cut_w)] + [img_w]
    for y0,y1 in F.pairwise(ys):
        for x0,x1 in F.pairwise(xs):
            yield (y0,x0, y1,x1) # NOTE: don't change order

import cv2
import unittest
class Test_make_trainalble(unittest.TestCase):
    def check_cut_method(self, img_h,img_w, cut_h,cut_w, expected):
        cuts = list(crop_coordseq(img_h,img_w, cut_h,cut_w))
        self.assertEqual(cuts, expected)
        for y0,x0,y1,x1 in cuts:
            self.assertTrue(img_h - y0 >= cut_h, (img_h, y0, cut_h))
            self.assertTrue(img_w - x0 >= cut_w, (img_w, x0, cut_w))
    
    def check_no_small_piece(
        self, img_h,img_w, cut_h,cut_w, expected):
        cuts = list(crop_coordseq(img_h,img_w, cut_h,cut_w))
        self.assertEqual(cuts, expected)

    def test_if_cut_hw_is_same_img_hw_then_no_cut(self):
        self.check_cut_method( 10,20, 10,20, [(0,0,10,20)] )
    #def test_if_cut_hw_is_greater_than_img_hw_then_no_cut(self):
        # NOTE: it never happen
        #self.check_cut_method( 10,20, 15,27, [(0,0,10,20)] )

    # cut h
    def test_if_img_h_is_2_of_cut_h_then_2cut_vertically(self):
        self.check_cut_method( 10,20, 5,20, [(0,0, 5,20), 
                                             (5,0,10,20)] )
    def test_if_img_h_is_3_of_cut_h_then_3cut_vertically(self):
        self.check_cut_method( 20,20, 5,20, [( 0,0, 5,20), 
                                             ( 5,0,10,20),
                                             (10,0,15,20),
                                             (15,0,20,20)] )
    # cut w
    def test_if_img_w_is_2_of_cut_w_then_2cut_horizontally(self):
        self.check_cut_method( 20,10, 20,5, [(0,0,20, 5), 
                                             (0,5,20,10)] )
    def test_if_img_w_is_3_of_cut_w_then_3cut_horizontally(self):
        self.check_cut_method( 20,20, 20,5, [(0, 0,20, 5), 
                                             (0, 5,20,10),
                                             (0,10,20,15),
                                             (0,15,20,20)] )
    # cut both
    def test_if_img_hw_is_exact_multiple_of_cut_hw(self):
        self.check_cut_method( 80,90, 20,30, [
            ( 0, 0,20,30), ( 0,30,20,60), ( 0,60,20,90),
            (20, 0,40,30), (20,30,40,60), (20,60,40,90),
            (40, 0,60,30), (40,30,60,60), (40,60,60,90),
            (60, 0,80,30), (60,30,80,60), (60,60,80,90),
        ])
    def test_if_img_hw_is_exact_multiple_of_cut_hw_w_slightly_long(self):
        self.check_cut_method( 80,93, 20,30, [
            ( 0, 0,20,30), ( 0,30,20,60), ( 0,60,20,93),
            (20, 0,40,30), (20,30,40,60), (20,60,40,93),
            (40, 0,60,30), (40,30,60,60), (40,60,60,93),
            (60, 0,80,30), (60,30,80,60), (60,60,80,93),
        ])
    def test_if_img_hw_is_exact_multiple_of_cut_hw_slightly_long(self):
        self.check_cut_method( 90,92, 20,30, [
            ( 0, 0,20,30), ( 0,30,20,60), ( 0,60,20,92),
            (20, 0,40,30), (20,30,40,60), (20,60,40,92),
            (40, 0,60,30), (40,30,60,60), (40,60,60,92),
            (60, 0,90,30), (60,30,90,60), (60,60,90,92),
        ])

    def test_if_img_hw_is_exact_multiple_of_cut_hw_slightly_long(self):
        self.check_cut_method(2819,2310, 900,700, [
            (   0,    0,  900,  700),
            (   0,  700,  900, 1400),
            (   0, 1400,  900, 2310),
            ( 900,    0, 1800,  700),
            ( 900,  700, 1800, 1400),
            ( 900, 1400, 1800, 2310),
            (1800,    0, 2819,  700),
            (1800,  700, 2819, 1400),
            (1800, 1400, 2819, 2310),
        ])
            
    #@unittest.skip('later')
    def test_real_img(self):
        img = cv2.imread('./fixtures/imgcut/1442000.jpg')
        ih,iw = img.shape[:2]
        print(ih,iw)
        for y0,x0, y1,x1 in crop_coordseq(ih,iw, 900,700):
            print('({:4d}, {:4d}, {:4d}, {:4d}),'.format(y0,x0, y1,x1))
            #print(y1 - y0, x1 - x0, 'x1', x1, 
                  #'iw - x0', iw - x0, 'iw - x1', iw - x1)
            cv2.imshow('cut', img[y0:y1, x0:x1])
            cv2.waitKey(0)


if __name__ == '__main__':
    unittest.main()
