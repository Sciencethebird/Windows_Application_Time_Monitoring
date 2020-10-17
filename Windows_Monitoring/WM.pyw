import os
import sys
import time
import pandas as pd
import numpy as np
import subprocess
from io import StringIO
from datetime import datetime
#from win10toast import ToastNotifier
#print(sys.version)

#To-Do
# add new process from csv, remove the need of dictionary init
# check all process at once
# total runtime

'''
running_minute={'Name': ['Chrome', 'Visual Studio' ,'OneNote', 'Overwatch', 'Python'],
                'Process': ['chrome.exe', 'devenv.exe', 'onenoteim.exe','Overwatch.exe', 'Python.exe'],
                'Time': [0, 0, 0, 0, 0]}
'''

def check_pocess(process):
    global history, df, history_file
    try:
        #print(history)
        df.loc[history['Process'][process]]
        #print(process, 'is running')
        history.at[process,'Time']+=1
        try:
            history.to_csv(history_file)
        except:
            pass
            #print('history.csv writing fails')
    except:
        pass
        #print(process, 'is not running')

# Set csv path
date = datetime.now().date()
history_file = 'history-'+ str(date)+'.csv'
folder = 'history'
history_file = os.path.join('C:/Users/Sciencethebird/Desktop/Side_Projects/Windows_Monitoring', folder, history_file)
#print(history_file)

format_file = os.path.join('C:/Users/Sciencethebird/Desktop/Side_Projects/Windows_Monitoring/format', 'format.csv')

while True:
    #print(datetime.now().date())

    # Run command : 'tasklist'
    try:
        result = subprocess.run(['start','/B','tasklist.exe'], stdout=subprocess.PIPE, shell= True).stdout
        result = result[158:].decode("utf-8")
    except:
        pass
    #print(result)
    
    # Parse stdout
    info = []
    lines  = StringIO(result).readlines()
    for line in lines:
        seg = line.split()
        temp = [' '.join(seg[:-5]),seg[-5],seg[-4],seg[-3], seg[-2]]
        info.append(temp)

    df = pd.DataFrame(np.array(info),
                   columns=['Process', 'PID', 'Session Name', 'Session', 'RAM'])
    df = df.set_index('Process')

    #print(df.sort_values(by = ['RAM']))

    try:
        if datetime.now().date() != date:
            date = datetime.now().date()
            history_file = 'history-'+ str(date)+'.csv'
            folder = 'history'
            history_file = os.path.join('C:/Users/Sciencethebird/Desktop/Side_Projects/Windows_Monitoring', folder, history_file)

        history = pd.read_csv(history_file)
        history = history.set_index('Name')
    except: 
       
        history = pd.read_csv(format_file) # when running first time
        history = history.set_index('Name')
        
    for index, _ in history.iterrows():
        check_pocess(index)

    time.sleep(60)

