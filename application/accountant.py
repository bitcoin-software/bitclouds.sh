from sseclient import SSEClient
import os
import datetime
import time

# the sparko endpoint, i.e. 'http://192.168.0.7:9737'
sparko = os.environ['SPARKO_ENDPOINT']

messages = SSEClient(sparko + '/stream', headers={'X-Access': os.environ['SPARKO_RO']})

for msg in messages:
    dtime = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
    if msg != '':
        print(str(dtime) + ":\n" + str(msg))
