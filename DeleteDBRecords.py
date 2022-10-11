import sqlite3

class DeleteDBRecords:
    def __init__(self):
        pass

    # Input must be three lists. The lists can either be empty or they can be lists of strings.
    @staticmethod
    def delete_by_criteria(stops: list, lines: list, dates: list):
        assert type(stops) == list
        assert type(lines) == list
        assert type(dates) == list


    @staticmethod
    def wipe_estimates_table():
        connection = sqlite3.Connection('transit_data.db')
        cur = connection.cursor()
        cur.execute('DROP TABLE IF EXISTS ESTIMATES')
        cur.execute("""CREATE TABLE IF NOT EXISTS ESTIMATES(
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
