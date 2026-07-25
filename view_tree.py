from database import get_db_connection

conn = get_db_connection()

cursor = conn.cursor()

cursor.execute("SELECT * FROM traversal_nodes")

rows = cursor.fetchall()

print("\n----- TRAVERSAL TREE -----\n")

for row in rows:
    print(dict(row))

conn.close()