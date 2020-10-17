import tkinter as tk
from datetime import datetime, timedelta
import os
import sys
import time
from pandas import DataFrame
import numpy as np
import subprocess
from io import StringIO
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import tkinter as Tk
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from pandas import read_csv
import os

#os.system('mode con: cols=20 lines=4')


font = {'family': 'serif',
        'color':  'forestgreen',
        'weight': 'normal',
        'size': 16,
        }
font2 = {'family': 'serif',
        'color':  'black',
        'weight': 'normal',
        'size': 10,
        }

window = tk.Tk()
window.title('SumTime!')
window.geometry('600x400')

history_file_date =datetime.now().date();
def plus_date():
    global history_file_date
    if(history_file_date == datetime.now().date()):
        return
    else:
        history_file_date = history_file_date+ timedelta(days = 1)

def minus_date():
  global history_file_date
  history_file_date = history_file_date+ timedelta(days = -1)   


fm = tk.Frame(window)
fm.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=1)

switch2 = tk.Button(fm, text='>', width=5, height=2, command=plus_date)     
switch2.pack(side=tk.RIGHT, expand=1, fill = tk.BOTH) 

switch = tk.Button(fm, text='hit me', width=15, height=2, command=None)     
switch.pack(side=tk.RIGHT, expand=1, fill = tk.BOTH) 
  
switch2 = tk.Button(fm, text='<', width=5, height=2, command=minus_date)     
switch2.pack(side=tk.RIGHT, expand=1, fill = tk.BOTH) 
  

status = tk.Label(window, font=('times', 20, 'bold'), bg='white', relief=tk.GROOVE )
status.pack(side=tk.BOTTOM, fill=Tk.BOTH, expand=1) 

fig = plt.Figure(figsize=(2, 3))

# variable for displaying today/ yesterday / past 7 day/



  
def turn_off(pid):
    try:
        subprocess.run(['taskkill', '/f', '/pid', pid], stdout=subprocess.PIPE)
        print('process off!')
        check_running(0)
    except:
        #pass
        print('close fail')
        check_running(0)
def turn_on(process):
    try: 
        p = subprocess.Popen(['pyw', '-3', 'C:/Users/Sciencethebird/Desktop/Side_Projects/Windows_Monitoring/WM.pyw'],shell= True, stderr = subprocess.PIPE)
        #print(p.stderr.decode("utf-8"))
        check_running(0)
        # p.wait()
        # time.sleep(0.5)
    except:
        # pass
        print('Fail Launching Process')
        #print(p.stderr)
        check_running(0)


def check_running(mode = 1):
    process = 'pythonw.exe'
    global window, status, switch
    result = subprocess.run(['start','/B','tasklist.exe'], stdout=subprocess.PIPE, shell= True).stdout
    result = result[158:].decode("utf-8")
    #print(window.grid_size(), 'lll')
    info = []
    lines  = StringIO(result).readlines()
    for line in lines:
        seg = line.split()
        temp = [' '.join(seg[:-5]),seg[-5],seg[-4],seg[-3], seg[-2]]
        info.append(temp)

    df = DataFrame(np.array(info),
                   columns=['Process', 'PID', 'Session Name', 'Session', 'RAM'])
    df = df.set_index('Process')
    #q.config(command = lambda:quit())
    try:
        try: 
            pid = df['PID'][process].iloc[0]
        except: 
            pid = df['PID'][process] #use iloc if you have multiple instance
        print("Running")
        status.config(text = 'Running', bg = 'forestgreen')
        switch.config(text = 'Turn Off')
        switch.config(command = lambda: turn_off(pid))

    except:
        print("Not Running")
        status.config(text = 'Not Running', bg = 'orangered')
        switch.config(text = 'Turn On')
        switch.config(command = lambda: turn_on(process))

    if mode: # after change status you don't want to put this in window again 
        window.after(10000,  check_running)


# Read CSV and plot canvas
def animate(i):

    global ax, animate_mode, history_file_date
    
    ax.clear()
    history_file ='history-'+ str(history_file_date)+'.csv'
    folder = 'history'
    history_file = os.path.join('C:/Users/Sciencethebird/Desktop/Side_Projects/Windows_Monitoring', folder, history_file)

    try:
        history = read_csv(history_file)
        history = history.set_index('Name')
    except:

        return
    if(history_file_date == datetime.now().date()):
        ax.set_title(str(history_file_date)+' (TODAY)', loc = 'right', fontdict = font)
    else:
        ax.set_title(history_file_date, loc = 'right', fontdict = font)
        ax.set_xlim((0, 1000) )
    labels = history.index.values
    ax.set_yticks( range(len(labels)) )
    ax.set_yticklabels(labels, fontdict = font2)
    


    # adjustime time showing position
    max = np.max(history['Time'].values) 
    for i, v in enumerate(history['Time'].values):
        if v > (max//2):
            ax.text(v*0.45, i-0.18, str('{:0>2d}'.format(v//60) )+":"+str('{:0>2d}'.format(v%60) ), color='white', fontweight='bold')
        else:
            ax.text(v+0.01*max, i-0.18, str('{:0>2d}'.format(v//60) )+":"+str('{:0>2d}'.format(v%60) ), color='black', fontweight='bold')
    
    ax.tick_params(top='off', bottom='off', left='off', right='off', labelleft='on', labelbottom='off')

    bars = ax.barh( np.arange( len(history['Time'].values) ), history['Time'].values, color = 'C0')  # update the data
    
    return bars

canvas = FigureCanvasTkAgg(fig, master=window)
canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)

fig.subplots_adjust(left=0.2)

ax = fig.add_subplot(111)

ani = animation.FuncAnimation(fig, animate, interval=500, blit=False)
check_running()
window.mainloop()

