import sqlite3
from scrape_truetime import get_stop_list

# Author: Jack Vandeleuv
# Knights of Ni Project

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# Calling the init_db function will delete/drop any existing database with the same name in its directory!
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


# DB schema here: https://docs.google.com/document/d/16u6fOXoH7vvdpqc0chSfZFtU7WNWvtZJj_QmHI8KwQc/edit?usp=sharing
# The init_db function creates a SQLite3 database in its own directory.
# This function only needs to be called once when the application is installed for the first time.
class CreateDB:
    def __init__(self):
        pass

    # Private method. Be careful when using, because you could wipe the database.
    @staticmethod
    def __make_db_with_stops():
        CreateDB.__make_empty_tables()  # Create three blank tables
        CreateDB.__fill_routes_and_stops()  # Scrape TrueTime and fill in all the current bus routes and stops

    # Private method. No risk of wiping database.
    @staticmethod
    def __confirm_empty_table_generated():
        connection = sqlite3.Connection('transit_data.db')
        cursor = connection.cursor()
        print('These tables are in the database currently:')
        cursor.execute('PRAGMA table_info(ROUTES)')
        print(cursor.fetchall())
        cursor.execute('PRAGMA table_info(STOPS)')
        print(cursor.fetchall())
        cursor.execute('PRAGMA table_info(ESTIMATES)')
        print(cursor.fetchall())
        connection.commit()

    # Private method. Be careful when using, because you could wipe the database.
    @staticmethod
    def __make_empty_tables():
        connection = sqlite3.Connection('transit_data.db')
        cursor = connection.cursor()

        cursor.execute('DROP TABLE IF EXISTS ROUTES')
        cursor.execute("""CREATE TABLE IF NOT EXISTS ROUTES(
        ROUTE_ID TEXT PRIMARY KEY,
        ROUTE_NAME TEXT
        )""")

        cursor.execute('DROP TABLE IF EXISTS STOPS')
        cursor.execute("""CREATE TABLE IF NOT EXISTS STOPS(
        STOP_ID TEXT PRIMARY KEY,
        STOP_NAME TEXT,
        DIRECTION TEXT
        )""")

        cursor.execute('DROP TABLE IF EXISTS ESTIMATES')
        cursor.execute("""CREATE TABLE IF NOT EXISTS ESTIMATES(
        ID INTEGER PRIMARY KEY,
        ETA INTEGER,
        TIME_CHECKED INTEGER,
        VEHICLE_ID STRING,
        PASSENGERS STRING,
        STOP_ID INTEGER,
        ROUTE_ID INTEGER,
        FOREIGN KEY (STOP_ID)
            REFERENCES STOPS(STOP_ID),
        FOREIGN KEY (ROUTE_ID)
            REFERENCES ROUTES(ROUTE_ID)
        )""")

        connection.commit()

    # Private method. Fills in routes and stops based on TrueTime website, using scrape_TrueTime.
    @staticmethod
    def __fill_routes_and_stops():
        list_of_dicts = get_stop_list()

        connection = sqlite3.Connection('transit_data.db')
        cursor = connection.cursor()

        route_set = set()
        for d in list_of_dicts:   # StopID: [StopName, Direction, RouteID, RoutName]
            for key, value in d.items():
                route_info = (value[2], value[3])
                # Add the information we care about for the ROUTES table into a set to ensure uniqueness
                route_set.add(route_info)

        stop_list = []
        stop_set = set()
        for d in list_of_dicts:
            for key, value in d.items():
                if key not in stop_set:
                    stop_list.append((key, value[0], value[1]))
                    stop_set.add(key)

        cursor.executemany('INSERT INTO ROUTES VALUES(?, ?)', route_set)
        cursor.executemany('INSERT INTO STOPS VALUES(?, ?, ?)', stop_list)

        connection.commit()


