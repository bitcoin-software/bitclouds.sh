from flask import Flask, jsonify, request
from sseclient import SSEClient
import pymongo
import requests
import json
import os
import datetime

dbclient = pymongo.MongoClient('localhost')
mongo_db = "tickets"
mongo = dbclient[mongo_db]

app = Flask(__name__)

app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.url_map.strict_slashes = False

sparko = os.environ['SPARKO_ENDPOINT']
messages = SSEClient(sparko + '/stream', headers={'X-Access': os.environ['SPARKO_RO']})


def notify(bot_message):

    def tgsend():
        tg_bot_token = os.environ['TG_TOKEN']
        tg_bot_chatID = os.environ['TG_CHAT']
        send_text = 'https://api.telegram.org/bot' + tg_bot_token + '/sendMessage?chat_id=' + \
                    tg_bot_chatID + '&parse_mode=Markdown&text=' + bot_message
        try:
            response = requests.get(send_text, timeout=3)
            if response.status_code == 200:
                msgsent = True
            else:
                msgsent = False
        except Exception as e_tg:
            print('telegram send error')
            print(e_tg)
            msgsent = False

        return msgsent

    try:
        headers = {
            'Content-Type': 'application/json',
        }

        data = '{"text": "' + bot_message + '"}'

        response = requests.post(os.environ['MSG_ENDPOINT'] + '/bcmon',
                                 headers=headers, data=data, verify=False, timeout=9)

        if response.status_code == 200:
            sent = True
        else:
            sent = tgsend()
    except Exception as e:
        print('matrix sent error')
        print(e)
        sent = tgsend()

    return sent


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

    return jsonify(params)


for msg in messages:
    dtime = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
    try:
        data = json.loads(msg.data)
        # check if price update
        print(dtime + ":\n" + str(data))
        if data['status'] == 'paid':
            print(data)
    except Exception:
        print('no data')

if __name__ == '__main__':
    app.run(debug=False, port=6677)

