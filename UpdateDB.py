import sqlite3
import timeit
import bs4
import requests
import re
import datetime
import cchardet as chardet  # This library speeds up html parsing

# Author: Jack Vandeleuv
# Knights of Ni Project

# This class allows you to continuously scrape TrueTime for minute-by-minute bus arrival estimates. It adds the
# resulting data into the transit_data.db database.


class UpdateDB:
    def __init__(self):
        pass

    # Private method that queries the database and packages the results together in a pandas Series of urls.
    @staticmethod
    def __get_urls_to_query(lines):
        route_subclause = " WHERE ROUTE_ID IN (\""

        if len(lines) == 1:
            route_subclause = f' WHERE ROUTE_ID = "{lines[0]}"'

        if len(lines) > 1:
            cs_lines = '","'.join(lines)
            route_subclause = route_subclause + cs_lines + "\")"

        connection = sqlite3.Connection('transit_data.db')
        cursor = connection.cursor()
        query = 'SELECT ROUTE_ID, DIRECTION, STOP_ID FROM STOPS ' + 'JOIN STOPS_ON_ROUTES USING(STOP_ID) JOIN ROUTES USING(ROUTE_ID)' + route_subclause
        print(query)
        cursor.execute(query)
        results = cursor.fetchall()
        connection.commit()

        urls_and_data = []
        for result in results:  # 71A, OUTBOUND, 8382
            url = 'https://truetime.portauthority.org/bustime/wireless/html/' \
                  'eta.jsp?route=Port+Authority+Bus%3A' + result[0] + '&direction' \
                '=Port+Authority+Bus%3A' + result[1] + '&id=Port+Authority+Bus%3A' + result[2] + '&showAllBusses=on'
            urls_and_data.append([result[0], result[1], result[2], url])

        return urls_and_data

    # Private helper function that takes in a url and outputs scraped data.
    @staticmethod
    def scrape_html_tags(session, url, tag, attribute):
        page = session.get(url)

        # Specify lxml parser to avoid different default parsers on different machines
        soup_object = bs4.BeautifulSoup(page.text, features='lxml')
        tagged_elements = soup_object.find_all(attribute, {'class': tag})

        result = []
        for element in tagged_elements:
            result.append(element.getText())

        return result

    @staticmethod
    def process_eta_text(eta_text):
        eta_list = []
        for index, string in enumerate(eta_text):
            if index % 2 == 0:
                route_search = re.search(r'^#\d+[a-zA-Z]*', string)
                if route_search is not None:
                    eta_list.append(route_search.group()[1:])
            if index % 2 != 0:
                if string == 'DUE':
                    eta_list.append(0)

                if string != 'DUE':
                    time_search = re.search(r'^\d+', string)
                    if time_search is not None:
                        eta_list.append(time_search.group())

        return eta_list

    @staticmethod
    def process_vehicle_text(vehicle_text):
        vehicle_data = []
        for string in vehicle_text:
            vehicle_no = re.search(r'Vehicle\s[0-9]+', string)  # Find bus id number
            if vehicle_no is not None:
                vehicle_string = vehicle_no.group()
                vehicle_data.append(vehicle_string[8:])

            passenger_info = re.search(r'Passengers:\s*[a-zA-Z]+\s*[a-zA-Z]+', string)  # Find the data about how full the bus is with passengers.
            if passenger_info is not None:
                pass_string = passenger_info.group()
                pass_items = pass_string.split('\t')
                vehicle_data.append(pass_items[-1])  # Last item in the list is the actual data

        return vehicle_data

    @staticmethod
    def scrape_estimates(lines):
        urls_and_data = UpdateDB.__get_urls_to_query(lines)
        session = requests.session()
        estimates = []

        # Every route/stop combo we're interested in is a list in urls_and_data
        for combo in urls_and_data:
            url = combo[3]
            current_time = str(datetime.datetime.now())
            strong_text = UpdateDB.scrape_html_tags(session, url, 'larger', 'strong')
            span_text = UpdateDB.scrape_html_tags(session, url, 'smaller', 'span')
            eta_data = UpdateDB.process_eta_text(strong_text)
            vehicle_data = UpdateDB.process_vehicle_text(span_text)

            # Bare-minimum check for scrape failure.
            if len(eta_data) % 2 == 0 and len(eta_data) == len(vehicle_data):
                routeno = combo[0]
                for index, data in enumerate(eta_data):
                    if data == routeno:   # If the scraped route id and the route id we're searching for match...
                        eta = eta_data[index + 1]
                        vehicleno = vehicle_data[index]
                        passengers = vehicle_data[index + 1]
                        stop_id = combo[2]
                        estimates.append((eta, current_time, vehicleno, passengers, stop_id, routeno))

        session.close()
        return estimates

    @staticmethod
    def update_db(estimates):
        connection = sqlite3.Connection('transit_data.db')
        cursor = connection.cursor()

        cursor.executemany('INSERT INTO ESTIMATES (ETA, TIME_CHECKED, VEHICLE_ID, PASSENGERS, STOP_ID, ROUTE_ID) VALUES(?, ?, ?, ?, ?, ?)', estimates)

        connection.commit()
