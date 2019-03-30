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
        assert order in ('incr','desc'), "'%s' is not 'incr' nor 'desc'" % order
        table = 'work_state'
        num_rows = self.num_rows(table)
        if num_rows == 0:
            self.db.execute(
                "INSERT INTO {} (id_order, now_id) VALUES ('{}','{}')"\
                .format(table, order, new_id)
            )
        else:
            cur = self.db.cursor()
            cur.execute(
                'SELECT id_order FROM %s' % table
            )
            saved_order = cur.fetchone()[0]
            assert saved_order == order, "saved_order:'%s' != '%s':arg_order" % (saved_order,order)

            self.db.execute(
                "UPDATE {} SET now_id = '{}' WHERE id_order = '{}'"
                .format(table, new_id, order)
            )

        assert self.num_rows(table) == 1, "Number of rows are not 1, something very weird happened! Notice it to db manager..."

    def clear_work_state(self):
        table = 'work_state'
        self.db.execute( "DELETE FROM {}" .format(table))
        assert self.num_rows(table) == 0, "Number of rows are not 0, something very weird happened! Notice it to db manager..."

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
        db.update_work_state('incr','1254000')
        db.clear_work_state()
        #db.update_work_state('ppap','1254000')
