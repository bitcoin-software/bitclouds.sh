from sseclient import SSEClient
import os
import datetime
import json
import threading
import re
from database import subscribe_host, find_hosts, deactivate_host, \
    get_hostdata, get_free_wan, init_host, register_payment, bind_ip
# the sparko endpoint, i.e. 'http://192.168.0.7:9737'
sparko = os.environ['SPARKO_ENDPOINT']

messages = SSEClient(sparko + '/stream', headers={'X-Access': os.environ['SPARKO_RO']})

BTCPRICE = 0


def create_host(name):
    newhost_data = get_hostdata(name)
    print("create host output: \n" + str(newhost_data))
    image = newhost_data['image']
    pwd = newhost_data['pwd']
    pub_key = newhost_data['init_pub']
    print("check image for " + name)
    if image == 'ubuntu-eu':
        print("get lan ip for " + name)
        lan_ip = os.popen('ssh nvme cbsd dhcpd').read().rstrip("\n")
        print(lan_ip)
        print("get wan ip for " + name)
        wan_ip = get_free_wan()
        print(wan_ip)
        print("bind ip for " + name)
        bind_ip(name, wan_ip)
        print("run ansible for " + name)
        print('/usr/local/bin/ansible-playbook /home/bitclouds/app/ansible/create_ubuntu.yml '
                  '--extra-vars="iname=' + name.replace('-', '_') + ' dname=' + name
                  + ' pwd=' + pwd + ' pub_key=\'' + pub_key + '\' lan_ip=\'' + lan_ip + '\' wan_ip=\'' + wan_ip + '\'"')
        os.system('/usr/local/bin/ansible-playbook /home/bitclouds/app/ansible/create_ubuntu.yml '
                  '--extra-vars="iname=' + name.replace('-', '_') + ' dname=' + name
                  + ' pwd=' + pwd + ' pub_key=\'' + pub_key + '\' lan_ip=\'' + lan_ip + '\' wan_ip=\'' + wan_ip + '\'"')
        print("init " + name)
        init_host(name, lan_ip, wan_ip)
        print("subscribe " + name)
        subscribe_host(name, 99)
    elif image == 'bitcoind':

        lan_ip = os.popen('ssh nvme cbsd dhcpd').read().rstrip("\n")
        wan_ip = get_free_wan()
        bind_ip(name, wan_ip)

        os.system('/usr/local/bin/ansible-playbook /home/bitclouds/app/ansible/create_bitcoind.yml '
                  '--extra-vars="iname=' + name.replace('-', '_') + ' dname=' + name
                  + ' pwd=' + pwd + ' pubkey=\'' + pub_key + '\' lan_ip=\'' + lan_ip + '\' wan_ip=\'' + wan_ip + '\'"')
        init_host(name, lan_ip, wan_ip)
        subscribe_host(name, 99)
    elif image == 'clightning':
        lan_ip = os.popen('ssh nvme cbsd dhcpd').read().rstrip("\n")
        wan_ip = get_free_wan()
        bind_ip(name, wan_ip)

        os.system('/usr/local/bin/ansible-playbook /home/bitclouds/app/ansible/create_clightning.yml '
                  '--extra-vars="iname=' + name.replace('-', '_') + ' dname=' + name
                  + ' pwd=' + pwd + ' pubkey=\'' + pub_key + '\' lan_ip=\'' + lan_ip + '\' wan_ip=\'' + wan_ip + '\'"')
        init_host(name, lan_ip, wan_ip)
        subscribe_host(name, 99)

    else:
        return False


def delete_host(name):
    todelete_hostdata = get_hostdata(name)
    image = todelete_hostdata['image']
    wan_ip = todelete_hostdata['wan_ip']
    if image == 'ubuntu-eu':
        os.system('/usr/local/bin/ansible-playbook /home/bitclouds/app/ansible/remove_vm.yml '
                  '--extra-vars="iname=' + name.replace('-', '_') + ' wan_ip=\'' + wan_ip + '\'"')
        deactivate_host(name)
    elif image == 'bitcoind':
        os.system('/usr/local/bin/ansible-playbook /home/bitclouds/app/ansible/remove_jail.yml '
                  '--extra-vars="iname=' + name.replace('-', '_') + ' wan_ip=\'' + wan_ip + '\'"')
        deactivate_host(name)
    else:
        return False


def decreaser():
    threading.Timer(60.0, decreaser).start()

    hosts = find_hosts()
    for host in hosts:
        #print(host)
        if host['balance'] > 0:
            subscribe_host(host['name'], -1)
        elif host['status'] == 'subscribed':
            delete_host(host['name'])


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
                print("host status: " + hostdata['status'])
                if hostdata['status'] == 'init':
                    print("creating host " + instance_name)
                    create_host(instance_name)
                elif hostdata['status'] == 'subscribed':
                    print("subscribing host " + instance_name)
                    subscribe_host(instance_name, sats)
            else:
                print('non-existent host topped up')

        print("paid invoice for:" + data['label'])

    except Exception as e:
        print("loading json exception: " + str(e))
