from database import get_db_connection

conn = get_db_connection()

cursor = conn.cursor()

cursor.execute("SELECT * FROM clicks")

rows = cursor.fetchall()

print("\n----- CLICKS TABLE -----\n")

for row in rows:
    print(dict(row))

conn.close()