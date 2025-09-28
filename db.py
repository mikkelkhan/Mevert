import pyodbc
from flask import g
from configparser import ConfigParser

config = ConfigParser()
config.read("config.ini")

# Ensure pyodbc connection pooling is enabled
pyodbc.pooling = True

def get_db_connection():
    """
    Return a per-request DB connection stored in Flask g.
    If it exists, reuse it; otherwise create a new one.
    """
    if 'db_conn' not in g:
        g.db_conn = pyodbc.connect(config["MSSQL"]["connect"])
    return g.db_conn

def get_db_cursor():
    """
    Return a new cursor from the per-request connection.
    """
    return get_db_connection().cursor()

def close_db_connection(e=None):
    """
    Close the DB connection at the end of the request.
    """
    conn = g.pop('db_conn', None)
    if conn is not None:
        conn.close()
