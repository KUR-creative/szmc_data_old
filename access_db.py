import sqlite3

class DB:
    def __init__(self, db_path):
        self.db = sqlite3.connect('szmc.db')
        self.db.execute('PRAGMA foreign_keys = ON;')
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_value, traceback):
        #print('closed well!')
        self.db.commit()
        self.db.close()

    def img_pathseq(self, get_sorted=True, incremental=True):
        cur = self.db.cursor()
        if get_sorted:
            if incremental:
                cur.execute('''SELECT id,file_path FROM image 
                    ORDER BY CAST(id AS INTEGER)''')
            else:
                cur.execute('''SELECT id,file_path FROM image 
                    ORDER BY CAST(id AS INTEGER) DESC''')
        else:        
            cur.execute('SELECT id,file_path FROM image')

        return cur.fetchall()

    def num_rows(self, table):
        cur = self.db.cursor()
        cur.execute('SELECT count(*) FROM %s' % table)
        n_rows = cur.fetchone()[0]
        return n_rows

    def update_work_state(self, order, new_id):
        table = 'work_state'
        num_rows = self.num_rows(table)
        if num_rows == 0:
            self.db.execute(
                "INSERT INTO {} (id_order, now_id) VALUES ('{}','{}')"\
                .format(table, order, new_id)
            )
        else:
            pass

        assert self.num_rows(table) == 1

if __name__ == '__main__':
    '''
    rows = img_pathseq()
    print(*rows, sep='\n')
    print('--------------------------------------------------')
    rows = img_pathseq(incremental=False)
    print(*rows, sep='\n')
    '''
    with DB('szmc.db') as db:
        print(db.num_rows('work_state'))
        db.update_work_state('incr','1117000')
