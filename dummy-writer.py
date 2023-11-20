import time
import os
import psycopg2
import loremipsum


# Fetching environment variables
DATABASE = os.getenv('POSTGRES_DATABASE', 'dummy')
PORT = int(os.getenv('POSTGRES_PORT', '5432'))
USER = os.getenv('POSTGRES_USER', 'dummy')
PASSWORD = os.getenv('POSTGRES_PASSWORD', 'mypassowrd')
HOST = os.getenv('POSTGRES_HOST', 'localhost')
TABLE = os.getenv('POSTGRES_TABLE', 'data')
SLEEP = int(os.getenv('SLEEP', '1'))


def insert(query: str):
    returning_id = None
    conn = None
    try:
        conn = psycopg2.connect(port=PORT, host=HOST,
                                database=DATABASE,
                                user=USER, password=PASSWORD,
                                )
        cur = conn.cursor()
        conn.autocommit = True
        cur.execute(query)
        returning_id = cur.fetchone()[0]
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    finally:
        if conn is not None:
            conn.close()

    return returning_id


def retry_insert(query: str, max_retries=5, delay=2):
    returning_id = None

    for retry in range(max_retries):
        returning_id = insert(query)
        if returning_id is None:
            time.sleep(delay)
            print("Retrying... {retry}".format(retry=retry))

    return returning_id


def init():
    sql = """CREATE DATABASE {database}""".format(database=DATABASE)
    insert(sql)

    sql = """
        CREATE TABLE IF NOT EXISTS
            {table}  (
                returning_id SERIAL PRIMARY KEY,
                data VARCHAR(200)
                )
        """.format(table=TABLE)
    insert(sql)


def insert_random_string():
    sentence = loremipsum.get_sentence().replace("'", "\"")
    sql = """
        INSERT INTO {table}(data)
        VALUES ('{sentence}')
        RETURNING returning_id;
        """.format(table=TABLE, sentence=sentence)

    return insert(sql)


if __name__ == '__main__':
    init()
    while True:
        print(insert_random_string())
        time.sleep(SLEEP)
