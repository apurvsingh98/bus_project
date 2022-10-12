import sqlite3

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
    def get_scraped_stops_based_on_route(route):
        assert type(route) == str

        connection = sqlite3.Connection('transit_data.db')
        cursor = connection.cursor()

        cursor.execute("SELECT STOP_ID, STOP_NAME "
                       "FROM STOPS JOIN ESTIMATES USING(STOP_ID) "
                       "WHERE ROUTE_ID = '" + route + "' "
                       "GROUP BY STOP_ID, STOP_NAME ORDER BY STOP_NAME")
        scraped_stops = cursor.fetchall()

        for i in range(len(scraped_stops)):
            # Pull out each individual stop_id/stop_name combo and turn the two-tuple into a list.
            scraped_stop_list = list(scraped_stops[i])
            # Convert each stop id into an int
            scraped_stop_list[0] = int(scraped_stop_list[0])
            # Insert the new list back into the data.
            scraped_stops[i] = scraped_stop_list

        connection.commit()

        return scraped_stops

    @staticmethod
    def get_scraped_days():
        connection = sqlite3.Connection('transit_data.db')
        cursor = connection.cursor()
        cursor.execute('SELECT DISTINCT(SUBSTR(TIME_CHECKED, 1, 10)) AS days FROM ESTIMATES ORDER BY days DESC')
        scraped_days = cursor.fetchall()
        connection.commit()

        for i in range(len(scraped_days)):
            day = scraped_days[i]
            scraped_days[i] = day[0]

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
    def test_data():
        # Here's the boilerplate code needed to query the database.
        connection = sqlite3.Connection('transit_data.db')
        cursor = connection.cursor()

        cursor.execute("""SELECT COUNT(STOP_ID) FROM STOPS""")

        results = cursor.fetchall()
        for r in results:
            print(r)

        connection.commit()

QueryDB.test_data()