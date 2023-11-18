import time
import psycopg2
import loremipsum
import os

# Fetching environment variables
DATABASE = os.getenv('POSTGRES_DATABASE', 'dummy')
PORT = int(os.getenv('POSTGRES_PORT', 5432))
USER = os.getenv('POSTGRES_USER', 'dummy')
PASSWORD = os.getenv('POSTGRES_PASSWORD', 'postgres')
HOST = os.getenv('POSTGRES_HOST', 'localhost')
TABLE = os.getenv('POSTGRES_TABLE', 'data')
SLEEP = int(os.getenv('SLEEP', 1))


def insert(query: str):
    id = None
    conn = None
    try:
        conn = psycopg2.connect(port=PORT, host=HOST,
                                database=DATABASE,
                                user=USER, password=PASSWORD,
                                )
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


def retry_insert(query: str, max_retries=5, delay=2):
    id = None

    for retry in range(max_retries):
        id = insert(query)
        if id is not None:
            break
        else:
            time.sleep(delay)

    return id


def init():
    sql = """CREATE DATABASE {database}""".format(database=DATABASE)
    insert(sql)

    sql = """
        CREATE TABLE IF NOT EXISTS
            {table}  (
                id SERIAL PRIMARY KEY,
                data VARCHAR(200)
                )
        """.format(table=TABLE)
    insert(sql)


def insert_random_string():
    sentence = loremipsum.get_sentence().replace("'", "\"")
    sql = """
        INSERT INTO {table}(data)
        VALUES ('{sentence}')
        RETURNING id;
        """.format(table=TABLE, sentence=sentence)

    return insert(sql)


if __name__ == '__main__':
    init()
    while True:
        print(insert_random_string())
        time.sleep(SLEEP)
