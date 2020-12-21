from flask import Flask, jsonify, request, current_app
import pymongo
import requests
import os
import datetime

dbclient = pymongo.MongoClient('localhost')
mongo_db = "tickets"
mongo = dbclient[mongo_db]

app = Flask(__name__)

app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.url_map.strict_slashes = False


def generate_invoice(amount_sats, desc):
    dtime = datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d-%H%M%S')

    headers = {
        'X-Access': os.environ['SPARKO_RO'],
    }

    data = '{"method": "invoice",' \
           ' "params": ["' + str(amount_sats*1000) + '", "' + dtime + '-' + desc + '", "' + desc + '@bitclouds"]}'

    response = requests.post(os.environ['SPARKO_ENDPOINT'] + '/rpc', headers=headers, data=data, verify=False)

    return response.json()


@app.route('/ticket')
def handle_data():
    invoice = generate_invoice(99, str(request.values.get('instance'))+"-support")['bolt11']
    params = {
        'instance': request.values.get('instance'),
        'email': request.values.get('email'),
        'msg': request.values.get('msg'),
        'invoice': invoice

    }

    #return jsonify(params)
    return current_app.send_static_file('')


if __name__ == '__main__':
    app.run(debug=False, port=6677)

