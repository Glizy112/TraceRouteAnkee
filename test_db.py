# from database import get_db_connection

# conn = get_db_connection()

# cursor = conn.cursor()

# cursor.execute("""
# INSERT INTO links(token,destination_url)
# VALUES (?,?)
# """,("abc123","https://google.com"))

# conn.commit()

# conn.close()

# print("Inserted")

from database import get_db_connection

conn = get_db_connection()

cursor = conn.cursor()

cursor.execute("SELECT * FROM links")

rows = cursor.fetchall()

for row in rows:
    print(dict(row))

conn.close()