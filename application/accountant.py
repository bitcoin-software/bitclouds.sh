from sseclient import SSEClient
import os
import datetime
import json
import threading
import re
from database import subscribe_host, find_hosts, deactivate_host, get_hostdata
# the sparko endpoint, i.e. 'http://192.168.0.7:9737'
sparko = os.environ['SPARKO_ENDPOINT']

messages = SSEClient(sparko + '/stream', headers={'X-Access': os.environ['SPARKO_RO']})

BTCPRICE = 0


def create_host(name):
    hostdata = get_hostdata(instance_name)
    image = hostdata['image']
    pwd = hostdata['pwd']
    pub_key = hostdata['init_pub']
    if image == 'ubuntu-eu':
        os.system('/usr/local/bin/ansible-playbook /home/bitclouds/app/ansible/create_ubuntu.yml '
                  '--extra-vars="iname=' + name.replace('-', '_') + ' dname=' + name
                  + ' pwd=' + pwd + ' pubkey=\'' + pub_key + '\'"')
        subscribe_host(name, 99)
    elif image == 'bitcoind':
        os.system('/usr/local/bin/ansible-playbook /home/bitclouds/app/ansible/create_bitcoind.yml '
                  '--extra-vars="iname=' + name.replace('-', '_') + ' dname=' + name
                  + ' pwd=' + pwd + ' pubkey=\'' + pub_key + '\'"')
        subscribe_host(name, 99)
    else:
        return False


def delete_host(name):
    hostdata = get_hostdata(instance_name)
    image = hostdata['image']
    pwd = hostdata['pwd']
    pub_key = hostdata['init_pub']
    if image == 'ubuntu-eu':
        os.system('/usr/local/bin/ansible-playbook /home/bitclouds/app/ansible/create_ubuntu.yml '
                  '--extra-vars="iname=' + name.replace('-', '_') + ' dname=' + name
                  + ' pwd=' + pwd + ' pubkey=\'' + pub_key + '\'"')
        subscribe_host(name, 99)
    elif image == 'bitcoind':
        os.system('/usr/local/bin/ansible-playbook /home/bitclouds/app/ansible/create_bitcoind.yml '
                  '--extra-vars="iname=' + name.replace('-', '_') + ' dname=' + name
                  + ' pwd=' + pwd + ' pubkey=\'' + pub_key + '\'"')
        subscribe_host(name, 99)
    else:
        return False



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
            sats = round(data['msatoshi_received']/1000)
            instance_name = extract_name(data['label'])
            print('adding balance to ' + instance_name)

            if get_hostdata(instance_name):
                hostdata = get_hostdata(instance_name)
                if hostdata['status'] == 'init':
                    create_host(instance_name)
                elif hostdata['status'] == 'subscribed':
                    subscribe_host(instance_name, sats)
            else:
                print('non-existent host topped up')

        print("paid invoice for:" + data['label'])

    except Exception as e:
        print("loading json exception: " + str(e))
