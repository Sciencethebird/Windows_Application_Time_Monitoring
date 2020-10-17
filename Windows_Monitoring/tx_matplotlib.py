from numpy import arange, sin, pi
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import tkinter as Tk
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from pandas import read_csv
import os


fig = plt.Figure(figsize = (5, 5))
root = Tk.Tk()
label = Tk.Label(root,text="SHM Simulation").grid(column=0, row=0)


def animate(i):
    history_file = 'history-2019-12-03-1'+'.csv'
    folder = 'history'
    history_file = os.path.join('C:/Users/Sciencethebird/Desktop/Side_Projects/Windows_Monitoring', folder, history_file)

    
    history = read_csv(history_file)
    history = history.set_index('Name')
    print(tuple(history.index.values) )
    print(history['Time'].values)
    
    ax.clear()
    labels = history.index.values
    print(len(labels))
    ax.set_yticks( range(len(labels)) )
    ax.set_yticklabels(labels)
    bars = ax.barh( np.arange( len(history['Time'].values) ), history['Time'].values)  # update the data
    return bars


canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().grid(column=0,row=1)

ax = fig.add_subplot(111)
fig.subplots_adjust(left=0.5)
y_pos = np.arange(6)

#ani = animation.FuncAnimation(fig, animate, np.arange(1, 200), interval=200, blit=False)
ani = animation.FuncAnimation(fig, animate, interval=200, blit=False)
Tk.mainloop()
