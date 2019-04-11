from access_db import DB
src_db_path = 'szmc_kkr190331.db'
dst_db_path = 'tmp.db'

with DB(src_db_path) as src_db, DB(dst_db_path) as dst_db:
    # get text != ? list from src
    # put text != ? list to dst
    src_db.get_worked_data()
    print(src_db.get_column_names('data'))
