import time
import psycopg2
from loremipsum import get_sentences

DATABASE = 'dummy'
PORT = 5432
USER = 'postgres'
HOST = 'localhost'
TABLE = 'data'


def insert(data: list):
    sql = """INSERT INTO {table}(data) VALUES(%s) RETURNING id;""".format(table=TABLE)
    conn = None
    vendor_id = None
    try:
        conn = psycopg2.connect(database=DATABASE, port=PORT,  user=USER, host=HOST)
        cur = conn.cursor()
        for line in data:
            cur.execute(sql, (line,))
        vendor_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return vendor_id

def create_database():
    sql = """CREATE DATABASE {database}""".format(database=DATABASE)
    conn = None
    try:
        conn = psycopg2.connect(port=PORT, user=USER, host=HOST)
        cur = conn.cursor()
        conn.autocommit = True
        cur.execute(sql)
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def create_table():
    sql = """CREATE TABLE IF NOT EXISTS {table}  (id SERIAL PRIMARY KEY, data VARCHAR(200))""".format(table=TABLE)
    conn = None
    try:
        conn = psycopg2.connect(database=DATABASE, port=PORT,  user=USER, host=HOST)
        cur = conn.cursor()
        conn.autocommit = True
        cur.execute(sql)
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

if __name__ == '__main__':
    create_database()
    create_table()
    while True:
        print(insert(get_sentences(1)))
        time.sleep(1)
