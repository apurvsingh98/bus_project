import unittest
import sqlite3
from DeleteDBRecords import DeleteDBRecords

class TestAvgWaitTimeGenerator(unittest.TestCase):

    def test_deleting_by_dates(self):
        DeleteDBRecords.delete_by_criteria([], [], ['2022-10-08','1010-10-10'])
        connection = sqlite3.Connection('transit_data.db')
        cur = connection.cursor()
        cur.execute("SELECT COUNT(ID) FROM ESTIMATES WHERE SUBSTR(TIME_CHECKED, 1, 10) IN ('2022-10-08','1010-10-10')")
        count_before = cur.fetchall()
        count_before = count_before[0][0]
        connection.commit()
        self.assertEqual(0, count_before)

    def test_deleting_by_stops(self):
        DeleteDBRecords.delete_by_criteria(['8280', '38', '8805'], [], [])
        connection = sqlite3.Connection('transit_data.db')
        cur = connection.cursor()
        cur.execute("SELECT COUNT(ID) FROM ESTIMATES WHERE STOP_ID IN (8280, 38, 8805)")
        count_before = cur.fetchall()
        count_before = count_before[0][0]
        connection.commit()
        self.assertEqual(0, count_before)

    def test_deleting_by_routes(self):
        DeleteDBRecords.delete_by_criteria([], ['71A', '71C'], [])
        connection = sqlite3.Connection('transit_data.db')
        cur = connection.cursor()
        cur.execute("SELECT COUNT(ID) FROM ESTIMATES WHERE ROUTE_ID IN ('71A', '71C')")
        count_before = cur.fetchall()
        count_before = count_before[0][0]
        connection.commit()
        self.assertEqual(0, count_before)

unittest.main()