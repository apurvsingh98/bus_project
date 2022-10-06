
import requests
from bs4 import BeautifulSoup
import json
import pandas as pd

httpSteelers = 'https://www.google.com/search?gs_ssp=eJzj4tDP1TcwLUnLNWD04iguSU3NSS0qBgA93AZ0&q=steelers&oq=steelers&aqs=chrome.1.0i271j46i131i433i512j35i39l2j0i131i433i512l4j0i512j0i131i433i512.2041j0j15&sourceid=chrome&ie=UTF-8#sie=t;/m/05tfm;6;/m/059yj;mt;fp;1;;;'
print(httpSteelers)
page = requests.get(httpSteelers)
soup = BeautifulSoup(page.content, 'html.parser')

table = soup.find_all('table')


#div class = "imspo_mt__pm-inf.imspo_mt__pm-infc.imspo_mt__date.imso-medium-font"
#div class = 'imso-hov'
#table class='ml-bs-u.liveresults-sports-immersive__match-grid'

# Scraping:
# Parse the page

# Find the required tag
#gameinfo = soup.find(id = "lb")
# Find the sub-tag
#table = gameinfo.find(class = 'imspo_mt__pm-inf.imspo_mt__pm-infc.imspo_mt__date.imso-medium-font')
#data = [table.get_text()]
#for d in data:
#    print(d)


#def sports_schedule():
#    date = input('Please enter a date in YYYY-MM-DD format: ')
#    pass
