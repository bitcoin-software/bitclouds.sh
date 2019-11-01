import os
import time
import datetime


def get_ips():
    result = list()

    jlist = os.popen("jls | egrep -o '[0-9]+.*192.168.0.[0-9]+'").read()

    lines = jlist.splitlines()

    for line in lines:
        jid = line.split('  ')[0]
        jip = line.split('  ')[1]
        print(jid + " has " + jip)


get_ips()