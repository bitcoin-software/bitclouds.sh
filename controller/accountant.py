import configparser

config = configparser.ConfigParser()

config.read('../controller/config.ini')

from ctrldbops import find_hosts, deduct_host, get_suspended, delete_host
from orchestrator import del_server

hosts = find_hosts()
for host in hosts:
    if host['status'] == 'subscribed':
        deduct_host(host['address'])
        print(host['address'] + "is subscribed; balance: " + str(host['balance']))
    last = host['address']


for host in get_suspended():
    delete_host(host['address'])
    del_server(host['address'])