# Intermediate Python Project
# Knights of Ni
# Abdul Rehman
# 5/10/2022

import requests
import json
from bs4 import BeautifulSoup
import pandas as pd 
import numpy as np
from datetime import date

# One and only weather function that takes an optional date and returns dates that 
# match the same weather conditions (temperature,precipitation) within a certain error range.

# ******* DATE FORMAT IS A STRING WITH THE FOLLOWING FORMAT: 'YYYY-MM-DD' *******

def get_matching_weather_dates(*args):

    # If no date is passed through, the current date will be used to for the reference weather conditions.

    # The following is the +- error bar for both temperature (celcius) and total precipitation 
    # sum for the day (in the future different bars for temperature and precipitation should be used)

    range = 3

    # *** The following code gathers the historic data from the weather API. The data only starts from 
    # 30-06-2022 and goes until the current day ***

    # Getting the current date into the current format for the API
    today = date.today()
    if len(str(today.day))==1:
        day ='0'+str(today.day)
    else:
        day = str(today.day)
    date_str = str(today.year)+'-'+str(today.month) +'-'+day
    # print(date_str)

    # The API call includes a latitude, longitude (for Pittsburgh), 
    # time zone, start and end date for which to gather data, 
    # attributes to gather: [daily max temperature, daily min temperature, daily precipitation sum]

    url=r'https://api.open-meteo.com/v1/forecast?latitude=40&longitude=-75.16&timezone=EST&start_date=2022-06-30&end_date='+date_str+'&daily=temperature_2m_max&daily=temperature_2m_min&daily=precipitation_sum&current_weather=True&daily=weathercode'
    headers={'Content-Type': 'application/json'}
    response = requests.get(url,headers=headers)
    data = json.loads(response.content.decode('utf-8'))

    # Averaging the daily maximum and minimum temperatures and extracting 
    # the data from the response from the API call

    temp = data['daily']['temperature_2m_max'] + data['daily']['temperature_2m_min']
    historic_avg_temp= [i *0.5 for i in temp]
    historic_precip_sum = data['daily']['precipitation_sum']

    # *** This concludes the historic weather data gathering. The code below deals
    # with gathering the reference date's weather data ***

    # The following lines determine whether there is an input date of interest
    # or if the current date is to be used

    if len(args)==0:
        today = date.today()
        range = 3
        if len(str(today.day))==1:
            day ='0'+str(today.day)
        else:
            day = str(today.day)
        date_str = str(today.year)+'-'+str(today.month) +'-'+day
    if len(args)==1:
        date_str=args[0]

    url1=r'https://api.open-meteo.com/v1/forecast?latitude=40&longitude=80&timezone=EST&start_date='+date_str+'&end_date='+date_str+'&daily=temperature_2m_max&daily=temperature_2m_min&daily=precipitation_sum&current_weather=True&daily=weathercode'

    headers={'Content-Type': 'application/json'}
    response1 = requests.get(url1,headers=headers)
    data1 = json.loads(response1.content.decode('utf-8'))

    temp1 = (data1['daily']['temperature_2m_max'][0] + data1['daily']['temperature_2m_min'][0])
    current_temp = temp1/2
    # print('Current temp:', current_temp)
    current_precip_sum = data1['daily']['precipitation_sum']
    current_precip_sum = current_precip_sum[0]
    # print('Current_precip:',current_precip_sum)

    # The following lines find the dates where the weather 
    # matches the weather conditions of the current day

    indices =[]
    index = 0
    for temp in (historic_avg_temp):
        try:
            if (current_temp>(historic_avg_temp[index]-range) and current_temp<(historic_avg_temp[index]+range)) and ((current_precip_sum>historic_precip_sum[index]-range) and (current_precip_sum<historic_precip_sum[index]+range)):
                indices.append(index)
        except:
            break
        index +=1 
    dates_of_interest=[]
    for index in indices:
        dates_of_interest.append(data['daily']['time'][index])

    # Returns a list of dates to be used to filter the wait times   

    # print(dates_of_interest)
    # print(len(dates_of_interest))
    return dates_of_interest

def main():
    get_matching_weather_dates()

if __name__ == "__main__":
    main()