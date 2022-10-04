import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import bs4
import sqlite3
import re
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
    # for link in links:
    #     print(link.string)
    print(soup.prettify())


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


# This function takes in a list of stop names and combines each one into a dict entry, with the id as key and the name
# as the value.
def zip_stop_id_and_name(url: str, direction: str, r_num: str, r_name: str) -> dict:
    page = requests.get(url)
    # Specify lxml parser to avoid different default parsers on different machines
    soup_object = bs4.BeautifulSoup(page.text, features='lxml')
    page_links = soup_object.find_all('a', attrs={'href': re.compile(r'^eta.jsp')})

    stop_info = {}
    for link in page_links:
        link_address = link.get('href')
        end_of_link = re.search(r'id=Port\+Authority\+Bus%3A[0-9]+', link_address).group()
        stop_id = re.search(r'A[0-9]+', end_of_link).group()
        stop_id = stop_id[1:]

        if not stop_id.isnumeric():
            raise Exception("Bad Stop Id!")

        stop_id = int(stop_id)
        stop_name_from_link = link.text
        stop_name = stop_name_from_link.strip()
        stop_info[stop_id] = [stop_name, direction, r_num, r_name]

    return stop_info


def scrape_dynamic_tag(url, class_name: str) -> List[str]:
    # This is boilerplate code that initializes a Chrome web driver for use by the Selenium library.
    options = Options()
    options.add_argument('--headless')
    service = Service(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)

    # Scrape the list of available routes from the TrueTime homepage using Selenium.
    result = []
    driver_result = driver.find_elements(By.CLASS_NAME, class_name)
    for r in driver_result:
        result.append(r.text)
    driver.quit()

    return result


def get_stop_list() -> List[dict]:
    url = 'https://truetime.portauthority.org/bustime/wireless/html/home.jsp'
    routes: List[str] = scrape_dynamic_tag(url, 'larger')  # Scrape the route names

    list_of_dicts = []

    for route in routes:
        print('Route:', route)
        r_elements = route.split('-')  # Split the route to get the route num, and route name
        r_name = r_elements[1].strip()
        r_num = r_elements[0].strip()  # The 0-index item in the list is the number

        # Check whether inbound and outbound are available for each route
        outbound, inbound = check_available_directions(r_num)

        # INBOUND and OUTBOUND are separate HTML pages that must be scraped separately.
        if outbound:
            url = f'https://truetime.portauthority.org/bustime/wireless/html/selectstop.jsp?route=Port+Authority+Bus%3A{r_num}&direction=Port+Authority+Bus%3AOUTBOUND'
            out_stop_names_and_ids: dict = zip_stop_id_and_name(url, 'OUTBOUND', r_num, r_name)
            list_of_dicts.append(out_stop_names_and_ids)

        if inbound:
            url = f'https://truetime.portauthority.org/bustime/wireless/html/selectstop.jsp?route=Port+Authority+Bus%3A{r_num}&direction=Port+Authority+Bus%3AINBOUND'
            in_stop_names_and_ids: dict = zip_stop_id_and_name(url, 'INBOUND', r_num, r_name)
            list_of_dicts.append(in_stop_names_and_ids)

    return list_of_dicts


cnt = 0
list_of_dicts = get_stop_list()
for d in list_of_dicts:
    for key in d.keys():
        cnt += 1
print(cnt)
# exploratory_scrape()
