from sseclient import SSEClient
import os
import datetime
import json
import threading
import re
from database import subscribe_host, find_hosts, deactivate_host

# the sparko endpoint, i.e. 'http://192.168.0.7:9737'
sparko = os.environ['SPARKO_ENDPOINT']

messages = SSEClient(sparko + '/stream', headers={'X-Access': os.environ['SPARKO_RO']})

BTCPRICE = 0


def decreaser():
    threading.Timer(60.0, decreaser).start()

    hosts = find_hosts()
    for host in hosts:
        if host['balance'] > 0:
            subscribe_host(host['name'], -1)
        elif host['status'] == 'subscribed':
            deactivate_host(host['name'])
        print(host)


def extract_name(label):
    match = re.search('([a-z]+-?[0-9]*)', label)
    try:
        name = match.group(0)
        return name
    except Exception as e:
        print("NAME EXTRACT ERROR: " + name)
        return False

### MAIN

decreaser()

for msg in messages:
    dtime = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
    try:

        data = json.loads(msg.data)

        #check if price update
        try:
            if int(float(data)):
                BTCPRICE = int(float(data))
                print('BTC PRICE UPDATE: ' + str(BTCPRICE))
            else:
                print("not digit")
        except Exception as e:
            print("price update exception: " + str(e))

        print(dtime + ":\n" + str(data))
        if data['status'] == 'paid':
            print(data['msatoshi_received'])
            sats = round(data['msatoshi_received']/1000)
            instance_name = extract_name(data['label'])
            print('adding balance to ' + instance_name)
            subscribe_host(instance_name, sats)
        print("paid invoice for:")
        print(data['label'])

    except Exception as e:
        print("loading json exception: " + str(e))
