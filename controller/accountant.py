import configparser

config = configparser.ConfigParser()

config.read('../controller/config.ini')

from dbops import find_hosts, deduct_host

hosts = find_hosts()
for host in hosts:
    if host['status'] == 'subscribed':
        deduct_host(host['address'])
        print(host['address'] + "is subscribed; balance: " + str(host['balance']))
