import configparser
import os
import datetime
import time
import sys

config = configparser.ConfigParser()

config.read('../controller/config.ini')

from ctrldbops import find_hosts, deduct_host, get_suspended, delete_host, get_bitbsd
from orchestrator import del_server

hosts = find_hosts()

if sys.argv[1] in ['new', 'subscribed', 'deleted', 'suspended']:
    for host in hosts:
        if host['status'] == sys.argv[1]:
            print(host)
elif sys.argv[1] == 'housekeeper':
    for host in hosts:
        if host['status'] == 'deleted':
            del_server(host['address'])
elif sys.argv[1] == 'del':
    host2del = sys.argv[2]
    for host in hosts:
        if host['address'] == host2del:
            delete_host(host['address'])
            del_server(host['address'])
