import os
import time
import datetime

def get_ssh():
    result = list()

    socklist = os.popen("sockstat -l4 | egrep -o '192.168.0.[0-9]+:6[0-9]+'").read()

    lines = socklist.splitlines()

    for line in lines:
        addr = line.split(":")
        record = {
            "host":addr[0],
            "port":addr[1]
        }
        result.append(record)

    return result


def get_rpc():
    result = list()

    socklist = os.popen("sockstat -l4 | egrep -o '192.168.0.[0-9]+:5[0-9]+'").read()

    lines = socklist.splitlines()

    for line in lines:
        addr = line.split(":")
        record = {
            "host": addr[0],
            "port": addr[1]
        }
        result.append(record)

    return result

state = dict()

state['ssh'] = get_ssh()
state['rpc'] = get_rpc()

## Jail BITCOIN_RPC port forward
#IP_JAIL="192.168.0.2"
#PORT_JAIL="{8332}"
#rdr pass on $IF_PUBLIC proto tcp from any to $IP_PUBLIC port $PORT_JAIL -> $IP_JAIL

dyn_path = '/etc/pf_dyn.conf'

while True:

    new_state = dict()
    new_state['ssh'] = get_ssh()
    new_state['rpc'] = get_rpc()

    if new_state != state:

        dtime = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
        print(dtime + ': state changed... overwriting PF rules...')
        state = new_state

        try:
            os.remove(dyn_path)
        except Exception:
            pass

        for record in new_state['ssh']:
            os.system("echo '## Jail BITCOIN_SSH port forward' >> " + dyn_path)
            os.system("echo 'IP_JAIL=\""+ record['host'] +"\"' >> " + dyn_path)
            os.system("echo 'PORT_JAIL=\"{" + record['port'] +"}\"' >> " + dyn_path)
            os.system("echo 'rdr pass on $IF_PUBLIC proto tcp from any to $IP_PUBLIC port $PORT_JAIL -> $IP_JAIL' >> " + dyn_path)

        for record in new_state['rpc']:
            os.system("echo '## Jail BITCOIN_RPC port forward' >> " + dyn_path)
            os.system("echo 'IP_JAIL=\""+ record['host'] +"\"' >> " + dyn_path)
            os.system("echo 'PORT_JAIL=\"{" + record['port'] +"}\"' >> " + dyn_path)
            os.system("echo 'rdr pass on $IF_PUBLIC proto tcp from any to $IP_PUBLIC port $PORT_JAIL -> $IP_JAIL' >> " + dyn_path)

    os.system('pfctl -f /etc/pf.conf')
    dtime = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
    print(dtime + ': PF reloaded')
    time.sleep(5)