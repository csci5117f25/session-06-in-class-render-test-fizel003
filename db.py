from flask import current_app, g 
from contextlib import contextmanager
import logging
import os
import psycopg2
from psycopg2.pool import ThreadedConnectionPool
from psycopg2.extras import DictCursor

pool = None

def setup():
    global pool
    DATABASE_URL = os.environ['DATABASE_URL']
    # current_app.logger.info(f"creating db connection pool")
    pool = ThreadedConnectionPool(1, 100, dsn=DATABASE_URL, sslmode='require')


@contextmanager
def get_db_connection():
    try:
        connection = pool.getconn()
        yield connection
    finally:
        pool.putconn(connection)


@contextmanager
def get_db_cursor(commit=False):
    with get_db_connection() as connection:
      cursor = connection.cursor(cursor_factory=DictCursor)
      # cursor = connection.cursor()
      try:
          yield cursor
          if commit:
              connection.commit()
      finally:
          cursor.close()

def add_entry (name, message):
    # Since we're using connection pooling, it's not as big of a deal to have
    # lots of short-lived cursors (I think -- worth testing if we ever go big)
    with get_db_cursor(True) as cur:
        # current_app.logger.info("Adding person %s", name)
        cur.execute("INSERT INTO guestbook (name, message) values (%s, %s)", (name, message))

def get_guestbook():
    retval = []
    with get_db_cursor(False) as cur:
        with get_db_cursor() as cur:
            cur.execute("select * from guestbook")
            for row in cur:
                retval.append({"name": row["name"], "message": row["message"]})
    return retval
    
setup()
get_guestbook()