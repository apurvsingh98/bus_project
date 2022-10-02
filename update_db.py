import requests
import sqlite3
import json

# Author: Jack Vandeleuv
# Knights of Ni Project


# The UpdateDB function queries the Pittsburgh Port Authority transit API and stores the result in a SQLite3 database in
# the same directory.
#
# This function does not write over existing data; instead, it appends new rows to the relevant tables with a timestamp
# about when the API call was executed.
#
# The API key hardcoded into this function can make a maximum of 10,000 requests per day.
# The API key is buLQAqbqJpnyLbq4vf5vkHtSf
def update_db():
    try:
        url = 'http://localhost:5040/bustime/api/v3/getrtpidatafeeds?key=buLQAqbqJpnyLbq4vf5vkHtSf'
        response = requests.get(url)
        print(type(response))
        for i in response:
            print(i)
        # response_txt = response.text
        # for char in response_txt:
        #     print(char)

    except PermissionError as pe:
        print(pe)

# I'm getting
update_db()
