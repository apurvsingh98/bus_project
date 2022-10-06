
import requests
from bs4 import BeautifulSoup
import json
import pandas as pd

# Explanation for Current Problem:
# I switched to a less complicated webpage (Steeler's home page) to get their schedule. Next step is getting it into a workable format.

httpSteelers = 'https://www.steelers.com/schedule/'
print(httpSteelers)
page = requests.get(httpSteelers)
soup = BeautifulSoup(page.content, 'html.parser')

game_info = soup.find_all(class_='nfl-o-matchup-cards__date-info')

for game in game_info:
    print(game)





#def sports_schedule():
#    date = input('Please enter a date in YYYY-MM-DD format: ')
#    pass
