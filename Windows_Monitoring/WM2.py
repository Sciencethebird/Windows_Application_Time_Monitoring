
import os
import sys
import time
import pandas as pd
import numpy as np
import subprocess
from io import StringIO
from datetime import datetime
import psutil
for proc in psutil.process_iter():
    try:
        # Get process name & pid from process object.
        processName = proc.name()
        processID = proc.pid
        print(processName , ' ::: ', processID)
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
        pass

    #time.sleep(5)

