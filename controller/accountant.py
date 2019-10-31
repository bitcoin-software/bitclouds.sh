import configparser
import os
import datetime

config = configparser.ConfigParser()

config.read('../controller/config.ini')

from ctrldbops import find_hosts, deduct_host, get_suspended, delete_host
from orchestrator import del_server

hosts = find_hosts()
for host in hosts:
    if host['status'] == 'subscribed':
        deduct_host(host['address'])
        dtime = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
        os.system("echo '" + dtime + ": " + host['address'] + "is subscribed; balance: " + str(host['balance']) + "' >> /tmp/acc.log")
    last = host['address']


for host in get_suspended():
    del_server(host['address'])
    delete_host(host['address'])