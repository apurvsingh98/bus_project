# Author: Abdul Rehman
# Knights of Ni Project

# Function(s) that get average wait times from the DB based on specific parameters from the user

import sqlite3
import os
import pandas as pd
from datetime import datetime

def avg_wait_time_generator (stop, line,**args):
        
    connection = sqlite3.Connection('transit_data.db')
    cursor = connection.cursor()
    cursor.execute('SELECT ETA, time_checked, stop_id,route_id,Vehicle_id FROM ESTIMATES WHERE STOP_ID =' + str(stop) +' AND ROUTE_ID = "'+line+ '"')
    results = cursor.fetchall()

    data_dict={'ETA':[], 
    'time_checked':[], 
    'stop_id':[],
    'route_id':[],
    'Vehicle_id':[]}

    for r in results:
        if type(r[0]) != int:
            data_dict['ETA'].append(0)
        else:
            data_dict['ETA'].append(r[0])
        data_dict['time_checked'].append(r[1])
        data_dict['stop_id'].append(r[2])
        data_dict['route_id'].append(r[3])
        data_dict['Vehicle_id'].append(r[4])
    
    data=pd.DataFrame(data_dict)
    first= 0 
    wait_times=[]
    for index, row in data.iterrows():
        if first!=0:
            delta = datetime.strptime(row['time_checked'],"%Y-%m-%d %H:%M:%S.%f") - datetime.strptime(start,"%Y-%m-%d %H:%M:%S.%f") 
            if delta.total_seconds()/60 > 30:
                last_bus =[]
                first = 0
            else:
                if row['ETA'] ==0 and row['Vehicle_id'] not in last_bus and row['time_checked'] != start:
                    
                    wait_times.append([delta.total_seconds()/60,row['stop_id'],row['route_id'],row['Vehicle_id'],row['time_checked'],row['time_checked'][:10]])
                    start = start = row['time_checked']
                    last_bus.append(row['Vehicle_id'])

                if row['ETA'] ==0 and row['Vehicle_id'] not in last_bus and row['time_checked'] == start:
                    if len(last_bus) ==5:
                        last_bus.pop(0)
                        last_bus.append(row['Vehicle_id'])
                    if len(last_bus) <5:
                        last_bus.append(row['Vehicle_id'])                

        if row['ETA']==0 and first ==0:
            start = row['time_checked']
            last_bus = [row['Vehicle_id']]
            first = 1
    return wait_times
    
def get_stop_ids(line):
    connection = sqlite3.Connection('transit_data.db')
    cursor = connection.cursor()
    cursor.execute('SELECT stop_id,route_id FROM ROUTES JOIN STOPS_ON_ROUTES USING(Route_ID) WHERE ROUTE_ID = "71C"')
    results = cursor.fetchall()
    return results

def get_all_wait_times_line(line):
    stops = get_stop_ids(line)
    wait_times =[]
    for stop in stops:
        wait_times.append(avg_wait_time_generator(stop[0],line))
    output_dict={'wait_time':[], 
    'stop_id':[],
    'route_id':[],
    'Vehicle_id':[],
    'time_checked':[],
    'day_checked':[],
    }
    for wait_time in wait_times:
        for stop in wait_time:
            output_dict['wait_time'].append(stop[0])
            output_dict['stop_id'].append(stop[1])
            output_dict['route_id'].append(stop[2])
            output_dict['Vehicle_id'].append(stop[3])
            output_dict['time_checked'].append(stop[4])
            output_dict['day_checked'].append(stop[5])
    output_data=pd.DataFrame(output_dict)
    # print(output_data.head(50))
    # print(output_data['wait_time'].mean())
    return output_data


def filtered_wait_time_averages(*args):
    if len(args)==3:
        data = get_all_wait_times_line(args[1])
        temp = data.loc[data['day_checked'].isin(args[2])]
        return temp['wait_time'].mean()
    else:
        data = get_all_wait_times_line(args[1])
        return data['wait_time'].mean()


def main():
    october_dates = ['2022-10-0'+str(i) for i in range(1,11)]
    # print(october_dates)
    print(filtered_wait_time_averages("overall","71C"))
    print(filtered_wait_time_averages("October","71C",october_dates,))
    # avg_wait_time_generator(8192,"71C")

if __name__ == "__main__":
    # os.chdir(r"/Users/arehman95/Desktop/CMU/Intermediate Python/PROJECT/")
    main()