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
        print(process, 'is running')
        history.at[process,'Time']+=1
        try:
            history.to_csv(history_file)
        except:
            print('history.csv writing fails')
    except:
        print(process, 'is not running')

# Set csv path
history_file = 'history-'+ str(datetime.now().date())+'.csv'
folder = 'history'
history_file = os.path.join(folder, history_file)
print(history_file)

format_file = os.path.join('format', 'format.csv')

while True:
    print(datetime.now().date())

    # Run command : 'tasklist'
    result = subprocess.run(['start','/B','tasklist.exe'], stdout=subprocess.PIPE, shell= True).stdout
    result = result[158:].decode("utf-8")
    print(result)
    
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
        history = pd.read_csv(history_file)
        history = history.set_index('Name')
    except: 
        print('New New New')
        history = pd.read_csv(format_file) # when running first time
        history = history.set_index('Name')
        #print(history)
    #check_pocess('Chrome')
    for index, _ in history.iterrows():
        check_pocess(index)

    time.sleep(5)

