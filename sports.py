import os

import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np


date_conversion = dict(zip(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']))

#Steeler's Schedule
'Pittsburgh Steeler\'s Home Schedule:'
httpSteelers = 'https://www.steelers.com/schedule/'
print(httpSteelers)
Steelpage = requests.get(httpSteelers)
Steelsoup = BeautifulSoup(Steelpage.content, 'html.parser')

game_info = Steelsoup.find_all(class_='nfl-o-matchup-cards__date-info')
weeks = list(game.getText().strip().split(' · ') for game in game_info)
weeks.pop(8) #bye week
game_dates = list('2022-'+ week[1][4:6] + '-' + week[1][7:] for week in weeks)
print(weeks)
game_location = Steelsoup.find_all(class_='nfl-o-matchup-cards__venue--location')
location_list = list(game.getText().strip() for game in game_location)

all_games = dict(zip(game_dates, location_list))

Steelers_home_games = {date:stadium for date,stadium in all_games.items() if stadium == 'Acrisure Stadium'}
Steelers_home_dates = list(date for date in Steelers_home_games.keys() if date != '')
print(Steelers_home_games, '\n')
#print(Steelers_home_dates, '\n')
#
# #Penguin's Schedule
print('Pittsburgh Penguins\' Home Schedule:')
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

formatted_dates = []
formatted_months = []
formatted_days = []
for date in Pens_home_dates:
    sub_list = date[:3], date[-2:]
    month = sub_list[0]
    if month in date_conversion.keys():
        month = date_conversion[month]
        formatted_months.append(month)
    else: pass
    day = sub_list[1]
    if day[0] == ' ':
        new_day = '0' + day[1]
        formatted_days.append(new_day)
    else:
        formatted_days.append(day)
formatted_dates = list('2022-' + formatted_months[i] + '-' + formatted_days[i] for i in range(len(formatted_months)))
Pens_home_games = dict(zip(formatted_dates, game_location))
print(Pens_home_games, '\n')

#University of Pittsburgh Panther's Schedule
print('University of Pittsburgh Panthers\' Home Schedule:')
column_list = ['Date', 'Time', 'At', 'Opponent', 'Location']
Panthers_schedule = pd.read_csv(r'pitt_football_homegames.txt')
Panthers_schedule.to_csv(r'pitt_football_homegames.csv')
new_schedule = Panthers_schedule.squeeze()
game_list = list(new_schedule.loc[i] for i in range(7))

new_game_list = []
dates = []
location = []

for item in game_list:
    item.split(' ')
    if item != '':
        new_game_list.append(item)
    else:
        pass
    item.strip()

for item in new_game_list:
    dates.append(item[:6])
for item in new_game_list:
    location.append(item[-16:])

formatted_dates = []
formatted_months = []
formatted_days = []
for date in dates:
    sub_list = date[:3], date[-2:]
    month = sub_list[0]
    if month in date_conversion.keys():
        month = date_conversion[month]
        formatted_months.append(month)
    else: pass
    day = sub_list[1]
    day.strip()
    if day[1] == ' ':
        new_day = '0' + day[0]
        formatted_days.append(new_day)
    else:
        formatted_days.append(day)
formatted_dates = list('2022-' + formatted_months[i] + '-' + formatted_days[i] for i in range(len(formatted_months)))

Panthers_home_games = dict(zip(formatted_dates, location))
print(Panthers_home_games)