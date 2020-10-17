# use Tkinter to show a digital clock
# tested with Python24    vegaseat    10sep2006
import tkinter as tk
from datetime import datetime
import os
import sys
import time
import pandas as pd
import numpy as np
import subprocess
from io import StringIO
#print(os.getcwd())
#subprocess.run(['cd', 'C:/Users/Sciencethebird/Desktop/Side_Projects/Windows_Monitoring'], stdout=subprocess.PIPE)

window = tk.Tk()
window.title('SumTime!')
window.geometry('250x200')

status = tk.Label(window, font=('times', 20, 'bold'), bg='white')
status.pack(fill=tk.BOTH, expand=1)

def switch_function():
    pass
    #print('lol')

def quit():
    global window
    window.destroy()

switch = tk.Button(window, text='hit me', width=15, height=2, command=switch_function)     
switch.pack()   

q = tk.Button(window, text='quit', width=15, height=2, command=quit)     
q.pack()   
    
def turn_off(pid):
    try:
        subprocess.run(['taskkill', '/f', '/pid', pid], stdout=subprocess.PIPE)
        #print('process off!')
    except:
        pass
        #print('close fail')
def turn_on(process):
    try: 
        subprocess.Popen(['pyw', '-3', 'WM.pyw'])
        #time.sleep(5)
    except:
        pass
        #print('Fail Launching Process')

def check_running(process):
    global window, status, switch
    result = subprocess.run(['start','/B','tasklist.exe'], stdout=subprocess.PIPE, shell= True).stdout
    result = result[158:].decode("utf-8")

    info = []
    lines  = StringIO(result).readlines()
    for line in lines:
        seg = line.split()
        temp = [' '.join(seg[:-5]),seg[-5],seg[-4],seg[-3], seg[-2]]
        info.append(temp)

    df = pd.DataFrame(np.array(info),
                   columns=['Process', 'PID', 'Session Name', 'Session', 'RAM'])
    df = df.set_index('Process')
    #q.config(command = lambda:quit())
    try:
        try: 
            pid = df['PID'][process].iloc[0]
        except: 
            pid = df['PID'][process] #use iloc if you have multiple instance
        #print("Running")
        status.config(text = 'Running')
        switch.config(text = 'Turn Off')
        switch.config(command = lambda: turn_off(pid))

    except:
        #print("Not Running")
        status.config(text = 'Not Running')
        switch.config(text = 'Turn On')
        switch.config(command = lambda: turn_on(process))

    window.after(100,  lambda: check_running(process))

check_running('pythonw.exe')
window.mainloop()
'''
while True:
    status.update()
    status.after(100)
    check_running('pythonw.exe')
'''
    
