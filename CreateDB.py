import sqlite3

# Author: Jack Vandeleuv
# Knights of Ni Project

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# Calling the init_db function will delete/drop any existing database with the same name!
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

# DB schema here: https://docs.google.com/document/d/16u6fOXoH7vvdpqc0chSfZFtU7WNWvtZJj_QmHI8KwQc/edit?usp=sharing


# The init_db function creates a SQLite3 database in its own directory.
# This function only needs to be called once when the application is installed for the first time.
class CreateDB:
    def __init__(self):
        pass

    @staticmethod
    def __init_db():
        connection = sqlite3.Connection('transit_data.db')
        cursor = connection.cursor()

        cursor.execute('DROP TABLE IF EXISTS routes')
        cursor.execute("""CREATE TABLE IF NOT EXISTS ROUTES(
        ROUTEID INTEGER PRIMARY KEY,
        ROUTENAME STRING
        )""")

