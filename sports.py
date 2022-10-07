
import requests
from bs4 import BeautifulSoup

# This code returns a dictionary of the date and stadium location for all Steeler's home games.
# It also returns a list of just the dates of Steeler's home games.

httpSteelers = 'https://www.steelers.com/schedule/'
print(httpSteelers)
page = requests.get(httpSteelers)
soup = BeautifulSoup(page.content, 'html.parser')

game_info = soup.find_all(class_='nfl-o-matchup-cards__date-info')
weeks = list(game.getText().strip().split(' · ') for game in game_info)
weeks.pop(8) #bye week
game_dates = list(week[1][4:] for week in weeks)

game_location = soup.find_all(class_='nfl-o-matchup-cards__venue--location')
location_list = list(game.getText().strip() for game in game_location)

all_games = dict(zip(game_dates, location_list))

steelers_home_games = {k:v for k,v in all_games.items() if v == 'Acrisure Stadium'}
steelers_home_dates = list(date for date in steelers_home_games.keys() if date != '')
print(steelers_home_games)
print(steelers_home_dates)

#def sports_schedule():
#    date = input('Please enter a date in YYYY-MM-DD format: ')
#    pass