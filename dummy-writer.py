import time
import psycopg2
import loremipsum
import os

# Fetching environment variables
DATABASE = os.getenv('DATABASE', 'dummy')
PORT = int(os.getenv('PORT', 5432))
USER = os.getenv('USER', 'dummy')
PASSWORD = os.getenv('PASSWORD', 'postgres')
HOST = os.getenv('HOST', 'localhost')
TABLE = os.getenv('TABLE', 'data')
SLEEP = int(os.getenv('SLEEP', 1))


def insert(query: str):
    conn = None
    id = None
    try:
        print(f'query={query}')

        print(f'connection: database={DATABASE}, \
            port={PORT}, \
            user={USER}, \
            password={PASSWORD}, \
            host={HOST}')

        cur = conn.cursor()
        conn.autocommit = True
        cur.execute(query)
        id = cur.fetchone()[0]
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    finally:
        if conn is not None:
            conn.close()
    return id


def create_database():
    sql = """CREATE DATABASE {database}""".format(database=DATABASE)
    insert(sql)


def create_table():
    sql = """
        CREATE TABLE IF NOT EXISTS
            {table}  (
                id SERIAL PRIMARY KEY,
                data VARCHAR(200)
                )
        """.format(table=TABLE)
    insert(sql)


def insert_random_string():
    sentence = loremipsum.get_sentence()
    print(sentence)
    sql = """
        INSERT INTO {table}(data)
        VALUES ("{string}")
        RETURNING id;
        """.format(table=TABLE, string=sentence)
    return insert(sql)


if __name__ == '__main__':
    create_database()
    create_table()
    while True:
        print(insert_random_string())
        time.sleep(SLEEP)
