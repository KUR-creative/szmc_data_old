import funcy as F
from access_db import DB

#db_path = sys.argv[1]
db_path = 'szmc.db'
if __name__ == '__main__':
    with DB(db_path) as db:
        cur = db.db.cursor()
        cur.execute('''
            SELECT image.file_path
            FROM data, image
            WHERE data.id = image.id
              and image.extension != 'gif'
              and (data.text = 'H' or data.text = 'N')
            ORDER BY CAST(data.id AS INT)
        ''')
        process = F.rcompose(
            F.cat,
            F.partial(F.map, lambda s: s+'\n'),
        )
        fpath_seq = process(cur.fetchall())
    with open('txt_HN_190411_nogif.flist','w') as f:
        f.writelines(fpath_seq)
