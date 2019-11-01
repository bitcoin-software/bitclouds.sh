import os
import time
import datetime

def get_ssh():
    result = list()

    socklist = os.popen("sockstat -l4 | egrep -o '192.168.0.[0-9]+:6[0-9]+'").read()

    lines = socklist.splitlines()
