# Author: Abdul Rehman
# Knights of Ni Project

# Function(s) that get average wait times from the DB based on specific parameters from the user

import sqlite3
import os
import pandas as pd
from datetime import datetime

def wait_time_generator (stop, line,**args):
        
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

def get_wait_times_stop (stops,line):
    wait_times =[]
    try:
        for stop in stops:
            wait_times.append(wait_time_generator(stop[0],line))
    except:
        for stop in stops:
            wait_times.append(wait_time_generator(stop,line))       

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
    # print(output_data)
    return output_data

def filtered_wait_time_averages_stops(*args):
    dict_to_return ={}
    # print(args[0])
    # Pass stops and line to get_wait_times_stop
    data = get_wait_times_stop(args[0],args[1])
    if len(args)==3:
        for stop in args[0]:
            temp = data.loc[data['day_checked'].isin(args[2])]
            temp1 = temp.loc[temp['stop_id']==stop]
            dict_to_return[stop]=temp1['wait_time'].mean()
        return dict_to_return
    if len(args)==2:
        for stop in args[0]:
            print(args[0])
            print(stop)
            temp1 = data.loc[data['stop_id']==stop]
            dict_to_return[stop]=temp1['wait_time'].mean() 
        return dict_to_return

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
        wait_times.append(wait_time_generator(stop[0],line))
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
    return output_data

def filtered_wait_time_averages_line(*args):
    # Accepts two arguments: line and date list
    if len(args)==2:
        data = get_all_wait_times_line(args[0])
        temp = data.loc[data['day_checked'].isin(args[1])]
        return temp['wait_time'].mean()
    # Accepts one argument: line
    else:
        data = get_all_wait_times_line(args[0])
        return data['wait_time'].mean()

def main():
    october_dates = ['2022-10-0'+str(i) for i in range(1,7)]
    print(october_dates)
    print(filtered_wait_time_averages_stops([8192,8193],"71C",october_dates))
    # print(filtered_wait_time_averages_line("71C"))
    # print(filtered_wait_time_averages_line("71C",october_dates))
    # wait_time_generator(8192,"71C")

if __name__ == "__main__":
    # os.chdir(r"/Users/arehman95/Desktop/CMU/Intermediate Python/PROJECT/")
    main()