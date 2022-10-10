import sqlite3

# Author: Jack Vandeleuv
# Knights of Ni Project


class QueryDB:
    def __init__(self):
        pass

    @staticmethod
    def get_available_routes():
        connection = sqlite3.Connection('transit_data.db')
        cursor = connection.cursor()
        cursor.execute('SELECT ROUTE_ID, ROUTE_NAME FROM ROUTES')
        available_routes = cursor.fetchall()
        connection.commit()

        return available_routes

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

        cursor.execute("""SELECT TIME_CHECKED FROM ESTIMATES WHERE SUBSTR(TIME_CHECKED, 1, 10) = "2022-10-05" LIMIT 100""")

        results = cursor.fetchall()
        for r in results:
            print(r)

        connection.commit()
