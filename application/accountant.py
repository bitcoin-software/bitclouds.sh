from sseclient import SSEClient
from database import subscribe_host, find_hosts, deactivate_host, \
    get_hostdata, get_free_wan, init_host, register_payment, bind_ip, init_sparko, init_bitcoind, \
    get_k8s, init_k8s

import os
import datetime
import json
import threading
import re
import string
import random
import requests

# the sparko endpoint, i.e. 'http://192.168.0.7:9737'
sparko = os.environ['SPARKO_ENDPOINT']

messages = SSEClient(sparko + '/stream', headers={'X-Access': os.environ['SPARKO_RO']})

BTCPRICE = 0

MARKET = ['k8s']


def notify(bot_message):
    try:
        headers = {
            'Content-Type': 'application/json',
        }

        data = '{"text": "'+ bot_message + '"}'

        response = requests.post(os.environ['MSG_ENDPOINT'] + '/msg',
                                 headers=headers, data=data, verify=False, timeout=9)

        if response.status_code == 200:
            sent = True
        else:
            sent = False
    except Exception as e:
        print('matrix sent error')
        print(e)
        tg_bot_token = os.environ['TG_TOKEN']
        tg_bot_chatID = os.environ['TG_CHAT']
        send_text = 'https://api.telegram.org/bot' + tg_bot_token + '/sendMessage?chat_id=' + \
                   tg_bot_chatID + '&parse_mode=Markdown&text=' + bot_message
        try:
            response = requests.get(send_text, timeout=3)
            if response.status_code == 200:
                sent = True
            else:
                sent = False
        except Exception as e_tg:
            print('telegram send error')
            print(e_tg)
            sent = False
    return sent


def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


def create_host(name):
    newhost_data = get_hostdata(name)
    print("create host output: \n" + str(newhost_data))
    image = newhost_data['image']
    pwd = newhost_data['pwd']
    pub_key = newhost_data['init_pub']
    print("check image for " + name)
    if image == 'ubuntu':
        print("get lan ip for " + name)
        lan_ip = os.popen('ssh nvme cbsd dhcpd').read().rstrip("\n")
        print(lan_ip)
        print("get wan ip for " + name)
        wan_ip = get_free_wan()
        print(wan_ip)
        print("bind ip for " + name)
        bind_ip(name, wan_ip)
        print("run ansible for " + name)
        print('/usr/local/bin/ansible-playbook /home/bitclouds/bitclouds.sh/ansible/create_ubuntu.yml '
                  '--extra-vars="iname=' + name.replace('-', '_') + ' dname=' + name
                  + ' pwd=' + pwd + ' pub_key=\'' + pub_key + '\' lan_ip=\'' + lan_ip + '\' wan_ip=\'' + wan_ip + '\'"')
        os.system('/usr/local/bin/ansible-playbook /home/bitclouds/bitclouds.sh/ansible/create_ubuntu.yml '
                  '--extra-vars="iname=' + name.replace('-', '_') + ' dname=' + name
                  + ' pwd=' + pwd + ' pub_key=\'' + pub_key + '\' lan_ip=\'' + lan_ip + '\' wan_ip=\'' + wan_ip + '\'"')
        print("init " + name)
        init_host(name, lan_ip, wan_ip)
        print("subscribe " + name)
        subscribe_host(name, 99)
    elif image == 'centos':
        lan_ip = os.popen('ssh nvme cbsd dhcpd').read().rstrip("\n")
        wan_ip = get_free_wan()
        bind_ip(name, wan_ip)
        os.system('/usr/local/bin/ansible-playbook /home/bitclouds/bitclouds.sh/ansible/create_centos.yml '
                  '--extra-vars="iname=' + name.replace('-', '_') + ' dname=' + name
                  + ' pwd=' + pwd + ' pub_key=\'' + pub_key + '\' lan_ip=\'' + lan_ip + '\' wan_ip=\'' + wan_ip + '\'"')
        init_host(name, lan_ip, wan_ip)
        subscribe_host(name, 99)
    elif image == 'debian':
        lan_ip = os.popen('ssh nvme cbsd dhcpd').read().rstrip("\n")
        wan_ip = get_free_wan()
        bind_ip(name, wan_ip)
        os.system('/usr/local/bin/ansible-playbook /home/bitclouds/bitclouds.sh/ansible/create_debian.yml '
                  '--extra-vars="iname=' + name.replace('-', '_') + ' dname=' + name
                  + ' pwd=' + pwd + ' pub_key=\'' + pub_key + '\' lan_ip=\'' + lan_ip + '\' wan_ip=\'' + wan_ip + '\'"')
        init_host(name, lan_ip, wan_ip)
        subscribe_host(name, 99)
    elif image == 'freebsd':
        lan_ip = os.popen('ssh nvme cbsd dhcpd').read().rstrip("\n")
        wan_ip = get_free_wan()
        bind_ip(name, wan_ip)
        os.system('/usr/local/bin/ansible-playbook /home/bitclouds/bitclouds.sh/ansible/create_freebsd.yml '
                  '--extra-vars="iname=' + name.replace('-', '_') + ' dname=' + name
                  + ' pwd=' + pwd + ' pub_key=\'' + pub_key + '\' lan_ip=\'' + lan_ip + '\' wan_ip=\'' + wan_ip + '\'"')
        init_host(name, lan_ip, wan_ip)
        subscribe_host(name, 99)
    elif image == 'freebsd-ufs':
        lan_ip = os.popen('ssh nvme cbsd dhcpd').read().rstrip("\n")
        wan_ip = get_free_wan()
        bind_ip(name, wan_ip)
        os.system('/usr/local/bin/ansible-playbook /home/bitclouds/bitclouds.sh/ansible/create_freebsd-ufs.yml '
                  '--extra-vars="iname=' + name.replace('-', '_') + ' dname=' + name
                  + ' pwd=' + pwd + ' pub_key=\'' + pub_key + '\' lan_ip=\'' + lan_ip + '\' wan_ip=\'' + wan_ip + '\'"')
        init_host(name, lan_ip, wan_ip)
        subscribe_host(name, 99)
    elif image == 'bitcoind':

        lan_ip = os.popen('ssh nvme cbsd dhcpd').read().rstrip("\n")
        wan_ip = get_free_wan()
        bind_ip(name, wan_ip)

        bitcoin_data = {
            'rpcuser': get_random_string(10),
            'rpc_pwd': get_random_string(10),
        }
        os.system('/usr/local/bin/ansible-playbook /home/bitclouds/bitclouds.sh/ansible/create_bitcoind.yml '
                  '--extra-vars="iname=' + name.replace('-', '_') + ' dname=' + name
                  + ' rpcuser=' + bitcoin_data['rpcuser'] + ' rpc_pwd=' + bitcoin_data['rpc_pwd']
                  + ' pwd=' + pwd + ' pub_key=\'' + pub_key + '\' lan_ip=\'' + lan_ip + '\' wan_ip=\'' + wan_ip + '\'"')
        init_host(name, lan_ip, wan_ip)
        init_bitcoind(name, bitcoin_data)
        subscribe_host(name, 99)
    elif image == 'clightning':
        lan_ip = os.popen('ssh nvme cbsd dhcpd').read().rstrip("\n")
        wan_ip = get_free_wan()
        bind_ip(name, wan_ip)

        sparko_data = {
            'login': get_random_string(10),
            'pwd_web': get_random_string(10),
            'pwd_rw': get_random_string(10),
            'pwd_ro': get_random_string(10),
        }

        os.system('/usr/local/bin/ansible-playbook /home/bitclouds/bitclouds.sh/ansible/create_clightning.yml '
                  '--extra-vars="iname=' + name.replace('-', '_') + ' dname=' + name
                  + ' sparko_login=' + sparko_data['login'] + ' sparko_pwd_web=' + sparko_data['pwd_web']
                  + ' sparko_pwd_rw=' + sparko_data['pwd_rw'] + ' sparko_pwd_ro=' + sparko_data['pwd_ro']
                  + ' pwd=' + pwd + ' pub_key=\'' + pub_key + '\' lan_ip=\'' + lan_ip + '\' wan_ip=\'' + wan_ip + '\'"')

        init_host(name, lan_ip, wan_ip)
        init_sparko(name, sparko_data)
        subscribe_host(name, 99)
    elif image == 'bsdjail':
        lan_ip = os.popen('ssh nvme cbsd dhcpd').read().rstrip("\n")
        wan_ip = get_free_wan()
        bind_ip(name, wan_ip)

        os.system('/usr/local/bin/ansible-playbook /home/bitclouds/bitclouds.sh/ansible/create_jail.yml '
                  '--extra-vars="iname=' + name.replace('-', '_') + ' dname=' + name
                  + ' pwd=' + pwd + ' pub_key=\'' + pub_key + '\' lan_ip=\'' + lan_ip + '\' wan_ip=\'' + wan_ip + '\'"')

        init_host(name, lan_ip, wan_ip)
        subscribe_host(name, 99)
    elif image in MARKET:
        if image == 'k8s':
            k8s_data = get_k8s()['data']
            init_k8s(name, k8s_data)
            subscribe_host(name, 99)
        else:
            return False
    else:
        return False


def delete_host(name):
    todelete_hostdata = get_hostdata(name)
    image = todelete_hostdata['image']
    wan_ip = todelete_hostdata['wan_ip']
    if image in ['ubuntu', 'freebsd', 'freebsd-ufs', 'debian', 'centos']:
        os.system('/usr/local/bin/ansible-playbook /home/bitclouds/bitclouds.sh/ansible/remove_vm.yml '
                  '--extra-vars="iname=' + name.replace('-', '_') + ' wan_ip=\'' + wan_ip + '\'"')
        deactivate_host(name)
    elif image in ['bitcoind', 'clightning', 'bsdjail']:
        os.system('/usr/local/bin/ansible-playbook /home/bitclouds/bitclouds.sh/ansible/remove_jail.yml '
                  '--extra-vars="iname=' + name.replace('-', '_') + ' wan_ip=\'' + wan_ip + '\'"')
        deactivate_host(name)
    elif image in MARKET:
        if image == 'k8s':
            try:
                requests.get(os.environ['K8S_LINK'] + '/api/v1/destroy/' + todelete_hostdata['k8s']['id'])
            except Exception:
                notify('failed to delete k8s cluster')
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
    match = re.search('[0-9]{8}-[0-9]{6}-([m-]{2}[a-z]+-?[0-9]*)|[0-9]{8}-[0-9]{6}-([a-z]+-?[0-9]*)', label)
    if match.group(1):
        name = match.group(1)
        return name
    elif match.group(2):
        name = match.group(2)
        return name
    else:
        print("NAME EXTRACT ERROR FROM LABEL: " + str(label))


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
