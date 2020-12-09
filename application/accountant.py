from sseclient import SSEClient
import os

# the sparko endpoint, i.e. '192.168.0.7:9737'
sparko = os.environ['SPARKO_ENDPOINT']

messages = SSEClient('https://' + sparko + '/stream', headers={'X-Access': os.environ['SPARKO_RO']})

for msg in messages:
    print(msg)
