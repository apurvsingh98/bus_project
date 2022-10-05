import sqlite3

# Author: Jack Vandeleuv
# Knights of Ni Project

connection = sqlite3.Connection('transit_data.db')
cursor = connection.cursor()

cursor.execute("""SELECT COUNT(STOP_ID) FROM STOPS""")
print(cursor.fetchall())
cursor.execute("""SELECT COUNT(ROUTE_ID) FROM ROUTES""")
print(cursor.fetchall())
cursor.execute("""SELECT COUNT(ROUTE_ID) FROM STOPS_ON_ROUTES""")
print(cursor.fetchall())

connection.commit()