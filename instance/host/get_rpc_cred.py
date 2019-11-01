import os
import random

with open("hnr1.abc","r") as fi:
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