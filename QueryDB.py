import sqlite3

# Author: Jack Vandeleuv
# Knights of Ni Project


# Here's the boilerplate code needed to query the database.
connection = sqlite3.Connection('transit_data.db')
cursor = connection.cursor()

# cursor.execute("""SELECT AVG(ETA) FROM ESTIMATES WHERE ETA != 'DUE' AND STOP_ID = 8192 AND ROUTE_ID = '71A'""")
cursor.execute('SELECT * FROM ESTIMATES')
results = cursor.fetchall()
for r in results:
    print(r)

connection.commit()
