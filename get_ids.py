# -*- encoding: utf-8 -*-
import json
from tqdm import tqdm
from itertools import chain
from pprint import pprint
from funcy import concat, map, filter, mapcat, partial, rcompose, lmap, tap, ignore
from funcy import flatten, rpartial, chunks
import unittest

#import sys, codecs
#sys.stdout = codecs.getwriter('utf8')(sys.stdout)
#sys.stderr = codecs.getwriter('utf8')(sys.stderr)

import os, re
def file_paths(root_dir_path):
    ''' generate file_paths of directory_path ''' 
    it = os.walk(root_dir_path)
    for root,dirs,files in it:
        for path in map(lambda name:os.path.join(root,name),files):
            yield path

def human_sorted(iterable):
    ''' Sorts the given iterable in the way that is expected. '''
    convert = lambda text: int(text) if text.isdigit() else text
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(iterable, key = alphanum_key)

def jsonpath2lines(jsonpath,encoding='UTF8'):
    with open(jsonpath, encoding=encoding) as f:
        return f.readlines()

def path_chunk2flist_file(chunk, file_name):
    with open(file_name, 'w') as f:
        return f.writelines(chunk)

tags2tag_names = partial(lmap, lambda dic: dic['name'])
has_tag = lambda t: lambda j: t in tags2tag_names(j['tags'])
id2imgname = lambda id: '/%04d/%d' % (id % 1000, id)
def id_ext2imgname(id_ext):
    id,ext = id_ext
    return '/%04d/%d.%s\n' % (id % 1000, id, ext)
#name2imgpath_tup = lambda name: name
#id2imgname = lambda id: str(id)

def main():
    jsons2id_ext_seq = rcompose(
        partial(mapcat, jsonpath2lines),
        partial(map, json.loads),
        partial(filter, has_tag('absurdres')),
        partial(filter, has_tag('monochrome')), # and
        partial(map, lambda j: (int(j['id']), j['file_ext']) )
    )

    jsons2017 = file_paths('./2017')
    jsons2018 = file_paths('./2018')
    json_paths = concat(jsons2017, jsons2018)
    #json_paths = ['./2017/2017000000000000.json', './2017/2017000000000001.json']
    id_ext_seq = jsons2id_ext_seq(json_paths)

    imgpaths = tqdm(map(id_ext2imgname, id_ext_seq), total=35000)
    path_chunk2flist_file(imgpaths, 'imgpaths.txt')
    '''
    for i,chunk in enumerate(ids2imgpath_chunks(ids)):
        path_chunk2flist_file(chunk, str(i)+'.txt')
    '''

    #ids -> imgnames -> imgpaths  -> chunk 8 -> write 8 file


# -> make files.txt
# -> 10 000 -> /0000/10000.png /0000/10000.jpg  
'''
'''
class Test(unittest.TestCase):
    def setUp(self):
        self.t_list = [
            {'category': '0', 'id': '540830', 'name': '1boy'},
            {'category': '0', 'id': '13200', 'name': 'black_hair'},
            {'category': '0', 'id': '1300281', 'name': 'male_focus'},
            {'category': '3', 'id': '3105', 'name': 'naruto'},
            {'category': '0', 'id': '397051', 'name': 'shirtless'},
            {'category': '0', 'id': '212816', 'name': 'solo'},
            {'category': '0', 'id': '464584', 'name': 'tattoo'},
            {'category': '4', 'id': '12564', 'name': 'uchiha_sasuke'},
            {'category': '1', 'id': '388407', 'name': 'yupii'}
        ]

    def test_has_tag(self):
        a_json = dict(tags=self.t_list)
        self.assertFalse(has_tag('absurdres')(a_json))

    def test_tags2tag_names(self):
        self.assertEqual(
            tags2tag_names(self.t_list),
            ['1boy', 'black_hair', 'male_focus', 'naruto', 'shirtless',
             'solo', 'tattoo', 'uchiha_sasuke', 'yupii']
        )

    def test_id2imgname(self):
        self.assertEqual(id2imgname(1000), '/0000/1000')
        self.assertEqual(id2imgname(1231000), '/0000/1231000')
        self.assertEqual(id2imgname(1231001), '/0001/1231001')
        self.assertEqual(id2imgname(7897321), '/0321/7897321')

    #def test_name2imgpath_tup(self):
        #self.assertEqual(name2imgpath_tup(1000), '/0000/1000')

if __name__ == '__main__':
    main()
    #unittest.main()

