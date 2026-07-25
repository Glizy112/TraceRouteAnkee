import sqlite3

conn = sqlite3.connect("database/traceroute.db")

cursor = conn.cursor()
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
conn.close()

print("Database Created Successfully")
