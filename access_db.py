import sqlite3
import numpy as np
import pandas as pd
from collections import namedtuple

def unzip(zipped):
    return zip(*zipped)

OrderId = namedtuple('OrderId','order id')
class DB:
    def __init__(self, db_path):
        self.db = sqlite3.connect(db_path)
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

    def get_work_state(self):
        table = 'work_state'
        cur = self.db.cursor()
        cur.execute(
            'SELECT * FROM %s' % table
        )

        order_id = cur.fetchone()
        if order_id is None:
            return None
        else:
            return OrderId(*order_id)

    def update_data(self, id, text):
        assert text in '?!OAHN'
        table = 'data'
        self.db.execute(
            "UPDATE {} SET text = '{}' WHERE id = '{}'"
            .format(table, text, id)
        )
        self.db.commit()

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
            saved_order = self.get_work_state().order
            assert saved_order == order, "saved_order:'%s' != '%s':arg_order" % (saved_order,order)

            self.db.execute(
                "UPDATE {} SET now_id = '{}' WHERE id_order = '{}'"
                .format(table, new_id, order)
            )

        assert self.num_rows(table) == 1, "Number of rows are not 1, something very weird happened! Notice it to db manager..."
        self.db.commit()

    def clear_work_state(self):
        table = 'work_state'
        self.db.execute( "DELETE FROM {}" .format(table))
        assert self.num_rows(table) == 0, "Number of rows are not 0, something very weird happened! Notice it to db manager..."
        self.db.commit()

    def get_column_names(self, table):
        cur = self.db.cursor()
        cur.execute('PRAGMA table_info({})'.format(table))
        schema = cur.fetchall()
        col_names = np.array(schema)
        return col_names[:,1]

    def get_data_where(self,where):
        table = 'data'
        cur = self.db.cursor()
        cur.execute(
            '''SELECT * 
               FROM data 
               WHERE {}
               ORDER BY CAST(id AS INT)'''.format(where))
        col_names = self.get_column_names(table)
        return pd.DataFrame(cur.fetchall(), columns=col_names)

    def get_worked_data(self):
        return self.get_data_where("text != '?'")

    '''
    def get_imgpaths_which(self, from_='data', where="data.text != '?'", 
                           orderby='CAST(data.id AS INT)'): #'' means INCR
        sql = #"""
            SELECT * 
            FROM {}
            WHERE {}
            ORDER BY {}
        #""".format(from_, where, orderby)
        cur = self.db.cursor()
        cur.execute(sql)
        return cur.fetchall()
    '''

    def unparted_raw_img_paths(self):
        #TODO: add 'parted(0/1)' column..
        cur = self.db.cursor()
        cur.execute('''
            SELECT data.id,image.file_path
            FROM data, image
            WHERE data.id = image.id
              and (data.text = 'H' or data.text = 'N')
            ORDER BY CAST(data.id AS INT)
        ''')
        return pd.DataFrame(cur.fetchall(), columns=['id','file_path'])

if __name__ == '__main__':
    '''
    rows = img_pathseq()
    print(*rows, sep='\n')
    print('--------------------------------------------------')
    rows = img_pathseq(incremental=False)
    print(*rows, sep='\n')
    '''
    with DB('tmp.db') as db:
        print(db.get_work_state())


        '''
        db.update_data('1117000','H')
        db.update_work_state('incr','1254000')
        print(db.get_work_state())
        db.clear_work_state(); input()
        db.update_work_state('incr','1254000'); input()
        db.update_work_state('incr','1117000'); input()
        db.clear_work_state(); input()
        db.update_work_state('incr','1320000'); input()
        db.update_work_state('incr','1442000'); input()
        db.clear_work_state(); input()
        '''

        #db.update_work_state('ppap','1254000')
