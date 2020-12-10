import requests
import os
import datetime


def generate_invoice(amount_sats, desc):
    dtime = datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d-%H%M%S')

    headers = {
        'X-Access': os.environ['SPARKO_RO'],
    }

    data = '{"method": "invoice",' \
           ' "params": ["' + str(amount_sats*1000) + '", "' + dtime + '-' + desc + '", "' + desc + '@bitclouds"]}'

    response = requests.post(os.environ['SPARKO_ENDPOINT'] + '/rpc', headers=headers, data=data, verify=False)

    return response.json()