import sqlite3

DATABASE = "database/traceroute.db"

def get_db_connection():
    #conn = get_db_connection()
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn