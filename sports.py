
import requests
from bs4 import BeautifulSoup

# This code returns a dictionary of the date and stadium location for all Steeler's home games.
# It also returns a list of just the dates of Steeler's home games.

#Steeler's Schedule
httpSteelers = 'https://www.steelers.com/schedule/'
print(httpSteelers)
Steelpage = requests.get(httpSteelers)
Steelsoup = BeautifulSoup(Steelpage.content, 'html.parser')

game_info = Steelsoup.find_all(class_='nfl-o-matchup-cards__date-info')
weeks = list(game.getText().strip().split(' · ') for game in game_info)
weeks.pop(8) #bye week
game_dates = list(week[1][4:] for week in weeks)

game_location = Steelsoup.find_all(class_='nfl-o-matchup-cards__venue--location')
location_list = list(game.getText().strip() for game in game_location)

all_games = dict(zip(game_dates, location_list))

Steelers_home_games = {date:stadium for date,stadium in all_games.items() if stadium == 'Acrisure Stadium'}
Steelers_home_dates = list(date for date in Steelers_home_games.keys() if date != '')
print(Steelers_home_games)
print(Steelers_home_dates, '\n')

#Penguin's Schedule
httpPens = 'https://www.ppgpaintsarena.com/events'
print(httpPens)
Penspage = requests.get(httpPens)
Penssoup = BeautifulSoup(Penspage.content, 'html.parser')

event_name = Penssoup.find_all(class_='title')
event_date = Penssoup.find_all(class_='m-date__singleDate')
all_events = list(event.getText().strip() for event in event_name)
all_event_dates = list(date.getText().strip().split('|')[0].strip() for date in event_date)
events = dict(zip(all_events, all_event_dates))
Pens_events = {name:date for name,date in events.items() if name[0:8] == 'Penguins'}
Pens_home_dates = list(Pens_events.values())
game_location = list(['PPG Paints Arena']*len(Pens_home_dates))
Pens_home_games = dict(zip(Pens_home_dates, game_location))
print(Pens_home_games)
print(Pens_home_dates)

#def sports_schedule():
#    date = input('Please enter a date in YYYY-MM-DD format: ')
#    pass