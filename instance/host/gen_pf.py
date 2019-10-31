import os
import time


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


ssh_state = get_ssh()
rpc_state = get_rpc()

## Jail BITCOIN_RPC port forward
#IP_JAIL="192.168.0.2"
#PORT_JAIL="{8332}"
#rdr pass on $IF_PUBLIC proto tcp from any to $IP_PUBLIC port $PORT_JAIL -> $IP_JAIL

dyn_path = '/etc/pf_dyn.conf'

try:
    os.remove(dyn_path)
except Exception:
    pass

for record in ssh_state:
    os.system("echo '## Jail BITCOIN_SSH port forward' >> " + dyn_path)
    os.system("echo 'IP_JAIL=\""+ record['host'] +"\"' >> " + dyn_path)
    os.system("echo 'PORT_JAIL=\"{" + record['port'] +"}\"' >> " + dyn_path)
    os.system("echo 'rdr pass on $IF_PUBLIC proto tcp from any to $IP_PUBLIC port $PORT_JAIL -> $IP_JAIL' >> " + dyn_path)


for record in rpc_state:
    os.system("echo '## Jail BITCOIN_RPC port forward' >> " + dyn_path)
    os.system("echo 'IP_JAIL=\""+ record['host'] +"\"' >> " + dyn_path)
    os.system("echo 'PORT_JAIL=\"{" + record['port'] +"}\"' >> " + dyn_path)
    os.system("echo 'rdr pass on $IF_PUBLIC proto tcp from any to $IP_PUBLIC port $PORT_JAIL -> $IP_JAIL' >> " + dyn_path)

