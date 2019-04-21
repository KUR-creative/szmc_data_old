'''
insert rows to db
This script used for creation of szmc.db 

create_db   -> szmc Schema
insert_rows -> szmc rows(data)
'''
import json
import sqlite3
from funcy import concat, map, filter, mapcat, partial, rcompose, lmap, tap, ignore, lfilter

from collections import namedtuple
def filename_ext(path):
    name_ext = namedtuple('name_ext','name ext')
    return name_ext( *os.path.splitext(os.path.basename(path)) )
def filename(path):
    return filename_ext(path).name
def extension(path):
    return filename_ext(path).ext

import os, re
def file_paths(root_dir_path):
    ''' generate file_paths of directory_path ''' 
    it = os.walk(root_dir_path)
    for root,dirs,files in it:
        for path in map(lambda name:os.path.join(root,name),files):
            yield path


interest_tags = ('highres','absurdres','comic',
                 'monochrome', 'greyscale')
def tag_names(tags):
    return lmap(lambda dic: dic['name'], tags)
def sql_dict(keys):
    val01s = map(lambda tag: int(tag in keys), interest_tags)
    return {k:v for k,v in zip(interest_tags,val01s)}


def insert2db(db_path, path_json_seq):
    def sql_val(x):
        if isinstance(x, int):
            return str(x)
        elif isinstance(x, str):
            return "\'"+str(x)+"\'"    
        else:
            raise ValueError('pass str or int')

    def insert_str(table,schema_tup,values_tup):
        assert len(schema_tup) == len(values_tup)
        schema = ','.join(schema_tup)
        values = ','.join([sql_val(n) for n in values_tup])
        return \
            'INSERT INTO {} ({}) VALUES ({})'.format(
                table, schema, values
            )
    def data_sql(id):
        return insert_str('data', ['id'], [id])
    def image_sql(id, path, ext, size, h, w):
        return insert_str(
            'image',
            ('id','file_path','extension',
             'file_size','height','width'),
            (id, path, ext, size, h, w)
        )
    def metadata_sql(id,highres=0,absurdres=0,comic=0,
                        monochrome=0,greyscale=0):
        return insert_str(
            'metadata',
            ('id',) + interest_tags,
            (id,highres,absurdres,comic,monochrome,greyscale)
        )

    with sqlite3.connect(db_path) as db:
        for path,j in path_json_seq:
            db.execute(tap( data_sql(j['id']) ))
            db.execute(tap( image_sql(
                j['id'], path, j['file_ext'], 
                int(j['file_size']),
                int(j['image_height']), int(j['image_width'])
            )))
            db.execute(tap( metadata_sql(
                j['id'], **sql_dict(tag_names( j['tags'] ))
            )))
        db.commit()

def main():
    dset_json_path = './absurdres_mono.json'
    with open(dset_json_path, 'r', encoding='utf8') as f:
        json_dic = json.load(f)

    def path_id2path_json(path_id):
        path,id = path_id
        return (path, json_dic[id])
    files2datas = rcompose(
        file_paths,
        list,
        partial( map, lambda p: p.replace('\\','/') ),
        partial( map, lambda p: (p,filename(p)) ),
        partial( map, path_id2path_json),
    )
    imgdir = 'danbooru_raw'
    insert2db( 'szmc.db', files2datas(imgdir) )


import unittest
class Test(unittest.TestCase):
    def setUp(self):
        dset_json_path = './absurdres_mono.json'
        with open(dset_json_path, 'r', encoding='utf8') as f:
            self.json_dic = json.load(f)
    def test_j2d(self):
        print( tag_names(self.json_dic['1441792']['tags']) )
        keys = tag_names(self.json_dic['1441792']['tags'])
        print(sql_dict(keys))
        keys = tag_names(self.json_dic['2529580']['tags'])
        print(sql_dict(keys))
        for id,j in self.json_dic.items():
            keys = tag_names(j['tags'])
            print(id, sql_dict(keys))

if __name__ == '__main__':
    #unittest.main()
    main()
