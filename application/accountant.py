from sseclient import SSEClient
import os
import datetime
import time
from database import add_host
from flask import jsonify

# the sparko endpoint, i.e. 'http://192.168.0.7:9737'
sparko = os.environ['SPARKO_ENDPOINT']

messages = SSEClient(sparko + '/stream', headers={'X-Access': os.environ['SPARKO_RO']})

for msg in messages:
    dtime = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
    print(str(dtime) + ":\n" + str(msg))
    try:
        data = jsonify(msg.data)
        if data['status'] == 'paid' and 'bitcolouds' in data['description']:
            add_host(data['description'], '135.125.129.128/26', 'password')
        print(msg.text.split(' '))

    except KeyError as e:
        print(e)
