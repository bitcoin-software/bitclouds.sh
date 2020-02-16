import requests
import json

from common import config

URL = config['lnurl']['url']
KEY = config['lnurl']['key']

def set_template(id, path_params, query_params, metadata, price_formula, webhook):
    r = requests.put(URL + '/template/' + id, auth=('api', KEY), data=json.dumps({
        'path_params': path_params,
        'query_params': query_params,
        'metadata': metadata,
        'price_satoshi': price_formula,
        'webhook': webhook
    }))
    r.raise_for_status()

def get_lnurl(template_id, params):
    r = requests.get(URL + '/template/' + template_id + '/lnurl',
        auth=('api', KEY),
        params=params
    )
    if not r.ok:
        return None
    return r.text
