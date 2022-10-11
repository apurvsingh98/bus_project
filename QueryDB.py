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
    def get_scraped_routes():
        connection = sqlite3.Connection('transit_data.db')
        cursor = connection.cursor()
        cursor.execute('SELECT DISTINCT(ROUTE_ID) FROM ESTIMATES')
        scraped_routes = cursor.fetchall()
        connection.commit()

        return scraped_routes

    @staticmethod
    def get_scraped_stops():
        connection = sqlite3.Connection('transit_data.db')
        cursor = connection.cursor()
        cursor.execute('SELECT DISTINCT(STOP_ID) FROM ESTIMATES')
        scraped_stops = cursor.fetchall()
        connection.commit()

        for i in range(len(scraped_stops)):
            # Index scraped_stops at [0] because scraped_stops is a list of one-tuples.
            stop = scraped_stops[i]
            scraped_stops[i] = stop[0]

        return scraped_stops

    @staticmethod
    def get_scraped_days():
        connection = sqlite3.Connection('transit_data.db')
        cursor = connection.cursor()
        cursor.execute('SELECT DISTINCT(SUBSTR(TIME_CHECKED, 1, 10)) AS days FROM ESTIMATES ORDER BY days DESC')
        scraped_days = cursor.fetchall()
        connection.commit()

        return scraped_days

    @staticmethod
    def count_estimates():
        connection = sqlite3.Connection('transit_data.db')
        cursor = connection.cursor()
        cursor.execute('SELECT COUNT(ID) FROM ESTIMATES')
        estimate_count = cursor.fetchall()
        connection.commit()

        return estimate_count

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

        # cursor.execute("""SELECT * FROM ESTIMATES WHERE SUBSTR(TIME_CHECKED, 1, 13) = '2022-10-08 14'""")

        cursor.execute("""SELECT * FROM ESTIMATES WHERE STOP_ID = 9334""")

        results = cursor.fetchall()
        for r in results:
            print(r)

        connection.commit()

QueryDB.count_data()