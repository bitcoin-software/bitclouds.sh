import os
import random

with open("/zroot/jails/jails-data/bitcoin_rpc-data/usr/local/etc/bitcoin.conf","r") as fi:
    lines = []
    for ln in fi:
        if ln.startswith("#guest_rpc"):
            id.append(ln[2:])

line = random.choice(lines)

data = line.split(' ')

credentials = {
    "user": data[1],
    "password": data[2]
    }

print(credentials['user'] + ' ' + credentials['password'])