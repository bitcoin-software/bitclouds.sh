import os
import random

lines = os.popen('cat /zroot/jails/jails-data/bitcoin_rpc-data/usr/local/etc/bitcoin.conf | grep #guest_rpc').read().splitlines()


line = random.choice(lines)

data = line.split(' ')

credentials = {
    "user": data[1],
    "password": data[2]
    }

print(credentials['user'] + ' ' + credentials['password'])