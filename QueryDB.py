import sqlite3

# Author: Jack Vandeleuv
# Knights of Ni Project


class QueryDB:
    def __init__(self):
        pass


    @staticmethod
    def count_data():
        # Here's the boilerplate code needed to query the database.
        connection = sqlite3.Connection('transit_data.db')
        cursor = connection.cursor()

        # cursor.execute("""SELECT AVG(ETA) FROM ESTIMATES WHERE ETA != 'DUE' AND STOP_ID = 8192 AND ROUTE_ID = '71A'""")
        # cursor.execute("""SELECT ROUTE_ID, STOP_ID, STOP_NAME, DIRECTION, AVG(ETA), COUNT(ID)
        # FROM ESTIMATES JOIN STOPS USING(STOP_ID)
        # WHERE ROUTE_ID = "71A"
        # GROUP BY stop_id
        # ORDER BY STOP_NAME DESC""")

        cursor.execute("""SELECT * FROM ESTIMATES ORDER BY ID DESC LIMIT 1000""")

        results = cursor.fetchall()
        for r in results:
            print(r)

        connection.commit()


QueryDB.count_data()