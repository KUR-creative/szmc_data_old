import sqlite3

# TODO: extract with, and get db as arg.
def img_pathseq(get_sorted=True, incremental=True):
    with sqlite3.connect('szmc.db') as db:
        db.execute('PRAGMA foreign_keys = ON;')
        cur = db.cursor()
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

def num_rows(table):
    with sqlite3.connect('szmc.db') as db:
        db.execute('PRAGMA foreign_keys = ON;')
        cur = db.cursor()
        cur.execute('SELECT count(*) FROM %s' % table)
        n_rows = cur.fetchone()[0]
        return n_rows

def update_work_state(order, new_id):
    pass

if __name__ == '__main__':
    '''
    rows = img_pathseq()
    print(*rows, sep='\n')
    print('--------------------------------------------------')
    rows = img_pathseq(incremental=False)
    print(*rows, sep='\n')
    '''
    print(num_rows('work_state'))
