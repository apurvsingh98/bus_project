import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import bs4
import sqlite3
from typing import List


# Author: Jack Vandeleuv
# Knights of Ni Project


# The UpdateDB function queries the Pittsburgh Port Authority transit API and stores the result in a SQLite3 database in
# the same directory.
#
# This function does not write over existing data; instead, it appends new rows to the relevant tables with a timestamp
# about when the API call was executed.
#
# The API key hardcoded into this function can make a maximum of 10,000 requests per day.
# The first API key the Port Authority sent is buLQAqbqJpnyLbq4vf5vkHtSf
# They sent a second one, which also doesn't work: PR22wm3bfA5mRjzy8aZdtYbbF
# url = 'http://localhost:8884/bustime/api/v3/gettime?key=buLQAqbqJpnyLbq4vf5vkHtSf'
def exploratory_scrape():
    url = f'https://truetime.portauthority.org/bustime/wireless/html/selectstop.jsp?route=Port+Authority+Bus%3A1&direction=Port+Authority+Bus%3AOUTBOUND'
    page = requests.get(url)
    # Specify lxml parser to avoid different defaults on different machines
    soup = bs4.BeautifulSoup(page.text, features='lxml')
    links = soup.find_all('a')  # Gets route and ETA, but not vehicle number
    for link in links:
        print(link.string)
    # print(soup.prettify())


# This function scrapes the TrueTime Port Authority Arrival Information System page for a list of currently available
# bus routes. This allows the update_db function to stay up-to-date if the available routes on the TrueTime page change.
def get_routes() -> List[str]:
    url = 'https://truetime.portauthority.org/bustime/wireless/html/home.jsp'
    routes = scrape_html_tag(url, 'strong')
    print(routes)


def check_available_directions(route_num: str) -> (bool, bool):
    url = f'https://truetime.portauthority.org/bustime/wireless/html/selectdirection.jsp?route=Port%20Authority%20Bus:{route_num}'
    page = requests.get(url)
    # Specify lxml parser to avoid different defaults on different machines
    soup = bs4.BeautifulSoup(page.text, features='lxml')
    soup = soup.text
    inbound = False
    outbound = False
    if 'OUTBOUND' in soup:
        outbound = True
    if 'INBOUND' in soup:
        inbound = True

    return outbound, inbound



# This function takes in a url and tag, and then scrapes the url for the given tag. It returns a list of strings,
# which contains every string found inside the given tag at the given url.
def scrape_html_tag(url, tag: str) -> List[str]:
    page = requests.get(url)
    # Specify lxml parser to avoid different default parsers on different machines
    soup_object = bs4.BeautifulSoup(page.text, features='lxml')
    tagged_elements = soup_object.find_all(tag)

    result = []
    for element in tagged_elements:
        result.append(element.string)
    return result


def scrape_dynamic_tag(url, class_name: str) -> List[str]:
    # This is boilerplate code that initializes a Chrome web driver for use by the Selenium library.
    options = Options()
    options.add_argument('--headless')
    service = Service(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)

    # Scrape the list of available routes from the TrueTime homepage using Selenium.
    routes = []
    results = driver.find_elements(By.CLASS_NAME, class_name)
    for r in results:
        routes.append(r.text)
    driver.quit()

    return routes


def get_stop_list() -> List[str]:
    url = 'https://truetime.portauthority.org/bustime/wireless/html/home.jsp'
    routes: List[str] = scrape_dynamic_tag(url, 'larger')  # Scrape the route names
    all_stops = []
    for route in routes:
        r_elements = route.split(' ')  # Split the route to get the route num, which is all we need for the next scrape
        r_num = r_elements[0]  # The 0-index item in the list is the number

        # Check whether inbound and outbound are available for each route
        outbound, inbound = check_available_directions(r_num)

        if outbound:
            url = f'https://truetime.portauthority.org/bustime/wireless/html/selectstop.jsp?route=Port+Authority+Bus%3A{r_num}&direction=Port+Authority+Bus%3AOUTBOUND'
            out_stops = scrape_html_tag(url, 'a')
            for string in out_stops:
                if string is not None:
                    string = string.strip()
                    if string.isupper():
                        all_stops.append(string)

        if inbound:
            url = f'https://truetime.portauthority.org/bustime/wireless/html/selectstop.jsp?route=Port+Authority+Bus%3A{r_num}&direction=Port+Authority+Bus%3AINBOUND'
            in_stops = scrape_html_tag(url, 'a')
            for string in in_stops:
                if string is not None:
                    string = string.strip()
                    if string.isupper():
                        all_stops.append(string)


    print('All stops:')
    print(len(all_stops))
    for stop in all_stops:
        print(stop)





get_stop_list()
# exploratory_scrape()
