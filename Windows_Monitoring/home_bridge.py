
import os
import sys
import time
import pandas as pd
import numpy as np
import subprocess
from io import StringIO
#from win10toast import ToastNotifier
env = os.environ
#running_tasks = os.system("homebridge")
print(os.getcwd())
#proc = subprocess.Popen("homebridge",shell = True, stdout=subprocess.PIPE)
#outs, errs = proc.communicate(timeout=15)
#print(outs)
#a = os.popen("homebridge").read()
#proc = subprocess.Popen("homebridge",shell = True, stdout=subprocess.PIPE)
proc = subprocess.Popen("homebridge",shell = True, stdout=subprocess.PIPE)

while True:
    try:
        outs = proc.stdout.read()
        #if len(outs) != 0:
        print(outs)
    except :
        proc.kill()
        outs, errs = proc.communicate()

        #print(sys.version)
    #running_tasks = os.system("homebridge")
    #result = subprocess.run(['homebridge'], stdout=subprocess.PIPE, shell = True).stdout
    #result = result.decode('utf-8')
    #print('a')
