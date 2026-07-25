import sqlite3
import init_db

DATABASE = "/tmp/traceroute.db"

def get_db_connection():
    #conn = get_db_connection()
    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()

    # Start building the database tables as soon as the server loads
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS links(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        token TEXT UNIQUE NOT NULL,
        destination_url TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS traversal_nodes(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    tracking_id TEXT,

    parent_tracking_id TEXT,

    generation INTEGER,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS clicks(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    tracking_id TEXT,

    ip_address TEXT,

    user_agent TEXT,

    browser TEXT,

    referer TEXT,

    clicked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )
    """)

    conn.commit()
    # conn.close()

    print("Database Created Successfully")

    # init_db()
    conn.row_factory = sqlite3.Row

    return conn