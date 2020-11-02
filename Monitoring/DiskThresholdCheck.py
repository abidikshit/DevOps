"""---DISK SPACE CHECK---
AUTHOR: Abhilash Dikshit
PUBLISHER: Abhilash Dikshit
VERSION: 1.0
RELEASE DATE: 1/9/2020
DESCRIPTION: Script will generate the log file once it reaches the threshold limit
"""

import subprocess
from datetime import datetime


# import sys
print('-'*60)
now = datetime.now()
dt = now.strftime("%d/%m/%Y %H:%M:%S")
print("Disk space usage on date:\n", dt)


def diskspace():
    threshold = 50
    child = subprocess.Popen(['df', '-h'], stdout=subprocess.PIPE)
    output = child.communicate()[0].strip().split('\n')
    for disk in output[1:]:
        if int(disk.split()[-2][:-1]) >= threshold:
            print(disk)


diskspace()

'''file = open('Disklog.log', 'w')
sys.stdout = file
print(diskspace())
file.close()'''
