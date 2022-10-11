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

        where_clause = ''

        for stop in stops:
            assert type(stop) == str

        for line in lines:
            assert type(line) == str

        for date in dates:
            assert type(date) == str

        if len(stops) != 0:
            stops_str = ",".join(stops)
            where_clause = " WHERE STOP_ID IN (" + stops_str + ")"

        if len(lines) != 0:
            lines_str = "','".join(lines)
            where_clause = " WHERE ROUTE_ID IN ('" + lines_str + "')"

        if len(dates) != 0:
            dates_str = "','".join(dates)
            where_clause = " WHERE SUBSTR(TIME_CHECKED, 1, 10) IN ('" + dates_str + "')"

        connection = sqlite3.Connection('transit_data.db')
        cur = connection.cursor()

        delete_query = "DELETE FROM ESTIMATES" + where_clause
        cur.execute(delete_query)

        connection.commit()

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
