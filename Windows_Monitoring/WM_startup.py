import subprocess

try:
    p = subprocess.Popen(['pyw', '-3', 'C:/Users/Sciencethebird/Desktop/Side_Projects/Windows_Monitoring/WM.pyw'],shell= True, stderr = subprocess.PIPE)
except:
    print("error")