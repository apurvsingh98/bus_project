import sqlite3

# Author: Jack Vandeleuv
# Knights of Ni Project


# The init_db function creates a SQLite3 database in its own directory.
# This function only needs to be called once when the application is installed for the first time.
# Note: Calling this function will delete/drop any existing database with the same name!
def init_db():
    connection = sqlite3.Connection('transit_data.db')

    cursor = connection.cursor()

    cursor.execute('DROP TABLE IF EXISTS ')

