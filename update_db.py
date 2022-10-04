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
    routes = scrape_html_tag(url, 'strong')
    print(routes)


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


def scrape_dynamic_tag(url, class_name: str = 'larger') -> List[str]:
    # This is boilerplate code that initializes a Chrome web driver for use by the Selenium library.
    options = Options()
    options.add_argument('--headless')
    service = Service(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)

    # Scrape the list of available routes from the TrueTime homepage using Selenium.
    routes = driver.find_elements(By.CLASS_NAME, class_name)
    for route in routes:
        print(route.text)
    driver.quit()


# This code tests the scrape_dynamic_tag function, which will feed into the other scraping function in this module.
url = 'https://truetime.portauthority.org/bustime/wireless/html/home.jsp'
scrape_dynamic_tag(url)
