import sqlite3
import init_db

DATABASE = "/tmp/traceroute.db"

def get_db_connection():
    #conn = get_db_connection()
    conn = sqlite3.connect(DATABASE)
    init_db()
    conn.row_factory = sqlite3.Row
    return conn