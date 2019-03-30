import sqlite3
def create_table(name='szmc.db'):
    with sqlite3.connect(name) as db:
        db.execute('PRAGMA foreign_keys = ON;')
        db.execute('''
        CREATE TABLE IF NOT EXISTS data(
            id      TEXT                                            PRIMARY KEY NOT NULL,
            text    TEXT CHECK( text IN ('?','!','O','A','H','N'))  NOT NULL DEFAULT '?',
            cnet    TEXT CHECK( cnet IN ('?','R','D','T')        )  NOT NULL DEFAULT '?',
            snet    TEXT CHECK( snet IN ('?','R','D','T')        )  NOT NULL DEFAULT '?'
        ); 
        ''')

        db.execute('''
        CREATE TABLE IF NOT EXISTS image(
            id          TEXT                                                PRIMARY KEY NOT NULL,
            file_path   TEXT                                                NOT NULL,
            extension   TEXT    CHECK( extension IN ('png','jpg','gif') )   NOT NULL,
            file_size   INTEGER CHECK( file_size > 0                    )   NOT NULL,
            height      INTEGER CHECK( height > 0                       )   NOT NULL,
            width       INTEGER CHECK( width > 0                        )   NOT NULL,
            FOREIGN KEY(id) REFERENCES data(id)
        ); 
        ''')

        db.execute('''
        CREATE TABLE IF NOT EXISTS metadata(
            id          TEXT                                    PRIMARY KEY NOT NULL,
            highres     INTEGER CHECK( highres    IN (0,1) )    NOT NULL DEFAULT 0,
            absurdres   INTEGER CHECK( absurdres  IN (0,1) )    NOT NULL DEFAULT 0,
            comic       INTEGER CHECK( comic      IN (0,1) )    NOT NULL DEFAULT 0,
            monochrome  INTEGER CHECK( monochrome IN (0,1) )    NOT NULL DEFAULT 0,
            greyscale   INTEGER CHECK( greyscale  IN (0,1) )    NOT NULL DEFAULT 0,
            FOREIGN KEY(id) REFERENCES data(id)
        ); 
        ''')

        db.execute('''
        CREATE TABLE IF NOT EXISTS work_state(
            id_order    TEXT CHECK( id_order IN ('incr','desc') )   NOT NULL,
            now_id      TEXT                                        NOT NULL,
            FOREIGN KEY(now_id) REFERENCES data(id)
        ); 
        ''')

        '''
        cursor = db.cursor()
        cursor.execute('SELECT * FROM tab')
        print(cursor.fetchone())
        print(cursor.fetchone())
        print(cursor.fetchone())
        print(cursor.fetchall())

        cursor.execute('SELECT * FROM tab')
        print(cursor.fetchall())
        '''
        db.commit()


if __name__ == '__main__':
    create_table()

