import sqlite3

# Author: Jack Vandeleuv
# Knights of Ni Project


# Here's the boilerplate code needed to query the database.
connection = sqlite3.Connection('transit_data.db')
cursor = connection.cursor()

# cursor.execute("""SELECT AVG(ETA) FROM ESTIMATES WHERE ETA != 'DUE' AND STOP_ID = 8192 AND ROUTE_ID = '71A'""")
cursor.execute('SELECT ROUTE_ID, AVG(ETA), COUNT(ID) FROM ESTIMATES GROUP BY ROUTE_ID ORDER BY AVG(ETA)')
results = cursor.fetchall()
for r in results:
    print(r)

connection.commit()
