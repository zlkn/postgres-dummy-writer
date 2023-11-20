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
DEBUG = os.getenv('DEBUG', 'false')


def insert(
        query: str,
        port: int = PORT, host: str = HOST,
        database: str = DATABASE,
        user: str = USER, password: str = PASSWORD
    ):
    returning_id = None
    conn = None

    if DEBUG == 'true':
        print(query)

    try:
        conn = psycopg2.connect(port=port, host=host,
                                database=database,
                                user=user, password=password,
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
    insert(query=sql, database='postgres')

    sql = """
        CREATE TABLE IF NOT EXISTS
            {table}  (
                id SERIAL PRIMARY KEY,
                data VARCHAR(200)
                )
        """.format(table=TABLE)
    insert(query=sql)


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
