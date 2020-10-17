
import os
import sys
print(sys.version)
import time
import pandas as pd
import numpy as np
import subprocess
from io import StringIO
from datetime import datetime
#from win10toast import ToastNotifier
print(sys.version)

#To-Do
# add new process from csv, remove the need of dictionary init
# check all process at once
# total runtime

running_minute={'Name': ['Chrome', 'Visual Studio' ,'OneNote', 'Overwatch', 'Python'],
                'Process': ['chrome.exe', 'devenv.exe', 'onenoteim.exe','Overwatch.exe', 'Python.exe'],
                'Time': [0, 0, 0, 0, 0]}

def check_pocess(process):
    global history, df, history_file
    try:
        #print(history)
        df.loc[history['Process'][process]]
        #print(process, 'is running')
        history['Time'][process]+=1
        #print(history)
        try:
            #os.path.join(os.getcwd(), history_file)
            history.to_csv(history_file)
        except:
            pass
            #print('history.csv writing fails')
    except:
        pass
        #print(process, 'is not running')

history_file = 'history-'+ str(datetime.now().date())+'.csv'
folder = 'history'
history_file = os.path.join(folder, history_file)
#pp = 'd'
#print(history_file)
while True:
    #pp+=pp
    #print(datetime.now().date())
    #running_tasks = os.system("tasklist")
    result = subprocess.run(['tasklist'], stdout=subprocess.PIPE).stdout
    #running_tasks = sys.argv
    #df = pd.read_csv(running_tasks , sep=" ")
    result = result[158:].decode("utf-8")
   # print(result)

   
    #while("" in result) : 
        #result.remove("") 
    info = []
    lines  = StringIO(result).readlines()
    for line in lines:
        seg = line.split()
        temp = [' '.join(seg[:-5]),seg[-5],seg[-4],seg[-3], seg[-2]]
        info.append(temp)
    #result = result.remove('')
    df = pd.DataFrame(np.array(info),
                   columns=['Process', 'PID', 'Session Name', 'Session', 'RAM'])
    df = df.set_index('Process')
    #print(df.sort_values(by = ['RAM']))

    try:
        history = pd.read_csv(history_file)
        #history = pd.DataFrame.from_dict(running_minute)
        history = history.set_index('Name')
    except: 
        history = pd.DataFrame.from_dict(running_minute) # when running first time or csv DNE
        history = history.set_index('Name')
        
    check_pocess('Chrome')
    check_pocess('Visual Studio')
    check_pocess('Overwatch')
    check_pocess('OneNote')
    start = 0
   
    time.sleep(2)
    #print()

'''
    try:
            #history = pd.read_csv('history.csv')
            history = pd.DataFrame.from_dict(running_minute, orient='index', columns=['Minute'])
            print(history)
    except:
            history = pd.DataFrame.from_dict(running_minute, orient='index', columns=['Minute'])

'''
