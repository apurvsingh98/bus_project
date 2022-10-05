import sqlite3

# Author: Jack Vandeleuv
# Knights of Ni Project


# Here's the boilerplate code needed to query the database.
connection = sqlite3.Connection('transit_data.db')
cursor = connection.cursor()

cursor.execute("""SELECT * FROM ESTIMATES""")
results = cursor.fetchall()
for r in results:
    print(r)

connection.commit()
