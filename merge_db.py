from access_db import DB
src_db_path = 'szmc_kkr190331.db'
dst_db_path = 'tmp.db'

with DB(src_db_path) as src_db, DB(dst_db_path) as dst_db:
    # get text != ? list from src
    # put text != ? list to dst
    dat = src_db.get_worked_data()
    print(dat)
    print('----')
    for row in dat['id']:
        print(row)
    #print(dat['id'])
    print(src_db.get_column_names('data'))
