import pyodbc
from flask import g
import logging
from configparser import ConfigParser

# Load DB config
config = ConfigParser()
config.read("config.ini")

# Enable pyodbc connection pooling for efficiency
pyodbc.pooling = True

def get_db_connection():
    """
    Return a per-request DB connection stored in Flask g.
    If it exists, reuse it; otherwise create a new one.
    """
    if 'db_conn' not in g:
        try:
            g.db_conn = pyodbc.connect(config["MSSQL"]["connect"])
        except Exception as e:
            logging.error(f"Failed to create DB connection: {e}")
            raise
    return g.db_conn


def execute_query(query, params=None, commit=False):
    """
    Execute a SQL query safely using parameters.

    :param query: SQL query string with '?' placeholders
    :param params: tuple of parameters to replace '?'
    :param commit: whether to commit the transaction (default: False)
    :return: list of results for SELECT, or rowcount for DML
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)

        # Determine query type
        if query.strip().lower().startswith("select"):
            return cursor.fetchall()
        else:
            if commit:
                conn.commit()
            return cursor.rowcount
    except Exception as e:
        logging.error(f"Database query error: {e}")
        raise
    finally:
        cursor.close()


def close_db_connection(e=None):
    """
    Close the per-request DB connection stored in Flask g.
    Called automatically at the end of request.
    """
    conn = g.pop('db_conn', None)
    if conn is not None:
        try:
            conn.close()
        except Exception as ex:
            logging.warning(f"Failed to close DB connection: {ex}")
