import sqlite3

def img_pathseq(get_sorted=True):
    with sqlite3.connect('szmc.db') as db:
        db.execute('PRAGMA foreign_keys = ON;')
        cur = db.cursor()
        if get_sorted:
            cur.execute('''SELECT id,file_path FROM image 
                           ORDER BY CAST(id AS INTEGER)''')
        else:        
            cur.execute('SELECT id,file_path FROM image')

        return cur.fetchall()

if __name__ == '__main__':
    rows = img_pathseq()
    print(*rows, sep='\n')
