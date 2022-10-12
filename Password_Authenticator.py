# -*- coding: utf-8 -*-
"""
Created on Fri Oct  7 17:55:05 2022

@author: apurv
"""
from tkinter import *
from functools import partial
import os.path
import mainMenuUI as mainMenu

def validateLogin(username, password):
    if os.path.isfile("Password.txt") == False:
        print("Password backup not found in - ",os.getcwd())
        print()
        
    else:
        with open("Password.txt","r") as f:
            global flag_username
            global flag_password
            
            flag_username = False
            flag_password = False
            
            for line in f:
                user, pw = line.split(" ") 
                pw = pw.rstrip("\n")
                if user == username.get():
                    flag_username = True
                    print("User Found")
                    
                    if pw == password.get():
 
                        flag_password = True
                        
                        print("User entered in the system")
                        tkWindow.destroy()
                        mainMenu.main()
                        
                    else:
                        
                        print("Incorrect password, try again")
                        
            if flag_username == False:
                
                user = str(username.get()) + " "
                user = user + str(password.get())
                user = user + '\n'
                f = open("Password.txt",'a+')
                f.write(user)
                f.close()
                print("User not found. Added user to the password database")
                tkWindow.destroy()
            
        
    
    

#window

tkWindow = Tk()  
tkWindow.geometry('400x150')  
tkWindow.title('AUTHENTICATOR')

#username label and text entry box
usernameLabel = Label(tkWindow, text="User Name ").grid(row=0, column=0)
print(usernameLabel)
username = StringVar()
usernameEntry = Entry(tkWindow, textvariable=username).grid(row=0, column=1)  

#password label and password entry box
passwordLabel = Label(tkWindow,text="Password ").grid(row=1, column=0)  
password = StringVar()
passwordEntry = Entry(tkWindow, textvariable=password, show='*').grid(row=1, column=1)  

validateLogin = partial(validateLogin, username, password)

#login button
loginButton = Button(tkWindow, text="Login", command=validateLogin).grid(row=7, column=2)  

tkWindow.mainloop()
