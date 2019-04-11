'''
python merge_db.py src dst
merge 'text' column of worked row of src to dst 
'''
from tqdm import tqdm
from access_db import DB
import sys
src_db_path = sys.argv[1]
dst_db_path = sys.argv[2]

with DB(src_db_path) as src_db, DB(dst_db_path) as dst_db:
    dat = src_db.get_worked_data()
    for id,text in tqdm(dat[['id','text']].itertuples(False),
                        total=len(dat)):
        dst_db.update_data(id,text)
