import configparser
import os
import datetime
import time
import sys

config = configparser.ConfigParser()

config.read('../controller/config.ini')

from ctrldbops import find_hosts, deduct_host, get_suspended, delete_host, get_bitbsd
from orchestrator import del_server

if sys.argv[1] in ['new', 'subscribed', 'deleted', 'suspended']:
    hosts = find_hosts()
    for host in hosts:
        if host['status'] == sys.argv[1]:
            print(host)
elif sys.argv[1] == 'housekeeper':
    hosts = find_hosts
    for host in hosts:
        if host['status'] == 'deleted':
            del_server(host['address'])