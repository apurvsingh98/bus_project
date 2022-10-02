import requests
from selenium import webdriver
import bs4
import sqlite3

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
# url = 'http://localhost:8884/bustime/api/v3/gettime?key=buLQAqbqJpnyLbq4vf5vkHtSf'
from typing import List


def update_db():
    url = 'https://truetime.portauthority.org/bustime/wireless/html/eta.jsp?route=Port+Authority+Bus%3A71A&direction=Port+Authority+Bus%3AINBOUND&id=Port+Authority+Bus%3A2635&showAllBusses=on'
    page = requests.get(url)
    # Specify lxml parser to avoid different defaults on different machines
    soup = bs4.BeautifulSoup(page.text, features='lxml')
    divs = soup.find_all('strong')  # Gets route and ETA, but not vehicle number
    for div in divs:
        print(div.string)


# This function scrapes the TrueTime Port Authority Arrival Information System page for a list of currently available
# bus routes. This allows the update_db function to stay up-to-date if the available routes on the TrueTime page change.
def get_routes() -> List[str]:
    url = 'https://truetime.portauthority.org/bustime/wireless/html/home.jsp'
    routes = scrape_tag(url, 'strong')
    print(routes)


# This function takes in a url and tag, and then scrapes the url for the given tag. It returns a list of strings,
# which contains every string found inside the given tag at the given url.
def scrape_tag(url, tag: str) -> List[str]:
    page = requests.get(url)
    # Specify lxml parser to avoid different default parsers on different machines
    soup_object = bs4.BeautifulSoup(page.text, features='lxml')
    tagged_elements = soup_object.find_all(tag)

    result = []
    for element in tagged_elements:
        result.append(element.string)
    return result


url = 'https://truetime.portauthority.org/bustime/wireless/html/home.jsp'
page = requests.get(url)
soup = bs4.BeautifulSoup(page.text, features='lxml')
print(soup.prettify())

# Note: this will be a point of failure if this program is installed on other machines.
driver = webdriver.Chrome('chromedriver_win32/chromedriver.exe')


divs = soup.find_all('strong')  # Gets route and ETA, but not vehicle number
for div in divs:
    print(div.string)

# get_routes()
