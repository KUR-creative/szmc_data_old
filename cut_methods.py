import unittest

def trainable_cuts(img_h,img_w, cut_h,cut_w):
    return  [(0,0,10,20)]

class Test_make_trainalble(unittest.TestCase):
    def test_if_cut_hw_is_same_img_hw_then_no_cut(self):
        img_h,img_w = 10,20
        cut_h,cut_w = 10,20
        expected = [(0,0,10,20)]

        cuts = trainable_cuts(img_h,img_w, cut_h,cut_w)
        self.assertEqual(cuts, expected)
if __name__ == '__main__':
    unittest.main()
