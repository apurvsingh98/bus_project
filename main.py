# -*- coding: utf-8 -*-
"""
Created on Wed Oct 12 00:52:56 2022

@author: apurv
"""

import UpdateDB
import timeit
import time
from UpdateDB import UpdateDB
from QueryDB import QueryDB
from avg_wait_time_generator import filtered_wait_time_averages_stops

import tkinter as tk
from tkinter import StringVar
from tkinter import *
import main as mainMenu



def Radioselected():
    if var_str.get() == 'radio1':
        
        master.destroy()
        mainMenu.scrape_window()
        
    elif var_str.get() == 'radio2':
        
        master.destroy()
        mainMenu.delete_data_window()
        
    elif var_str.get() == 'radio3':
        
        master.destroy()
        mainMenu.get_avg_frequency_by_criteria()
        
def main():
    global master
    master = Tk()
    master.title('Main Menu')
    master.geometry("500x350")
    l = Label(master, text = "Transit bus tracker")
    l.config(font =("Courier", 14))
    
     
    # Tkinter string variable
    # able to store any string value
    global var_str 
    var_str = StringVar()
     
    # Dictionary to create multiple buttons
    values = {"Scrape new data" : "radio1",
              "Delete existing data" : "radio2",
              "Explore existing data" : "radio3",
              }
     
    # Loop is used to create multiple Radiobuttons
    # rather than creating each button separately
    for (text, value) in values.items():
        Radiobutton(master, text = text, variable = var_str,
                    value = value, indicator = 0,
                    background = "light blue",command=Radioselected,height=5, width=20).pack(fill = X, ipady = 5)
     
    # Infinite loop can be terminated by
    # keyboard or mouse interrupt
    # or by any predefined function (destroy())
    l.pack()
    mainloop()

  

if __name__ == '__main__':
    main()


