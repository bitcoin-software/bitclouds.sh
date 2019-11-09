import configparser
import os
import datetime
import time
import sys

config = configparser.ConfigParser()

config.read('../controller/config.ini')

from ctrldbops import find_hosts, deduct_host, get_suspended, delete_host, get_bitbsd, hardclear
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
elif sys.argv[1] == 'housekeeper':
    for host in get_bitbsd('rootshell'):
            print(host)
    for host in get_bitbsd('lightningd'):
            print(host)
elif sys.argv[1] == 'del':
    host2del = sys.argv[2]
    for host in hosts:
        if host['address'] == host2del:
            delete_host(host['address'])
            del_server(host['address'])
elif sys.argv[1] == 'hardclear':
    many = int(input('how many hosts to delete?: '))

    while many > 1:
        print('hosts left to delete: ' + str(many))
        many -=1
        hardclear()

    print('deletion done')
