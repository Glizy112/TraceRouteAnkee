from database import get_db_connection

conn = get_db_connection()

cursor = conn.cursor()

cursor.execute("SELECT * FROM links")

rows = cursor.fetchall()

print("\n----- LINKS TABLE -----\n")

for row in rows:
    print(dict(row))

conn.close()