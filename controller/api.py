from flask import Flask
from flask_restful import Resource, Api, reqparse, request
from hashlib import blake2b
import requests
import datetime
import sys
import configparser

app = Flask(__name__)
api = Api(app)

config = configparser.ConfigParser()
config.read('../controller/config.ini')

wallet_host = config['wallet']['host']
project_path = config['paths']['local_path']
sys.path.insert(1, project_path + '/wallet')

# charge.py
#invoice(msat=None, amount=0, cur='EUR', desc=False)
#register_webhook(invoice_id, callback_url):
from charge import invoice, register_webhook


class CreateVPS(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('type')
        args = parser.parse_args()
        dtime = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
        try:
            host_type = args['type']
        except KeyError as e:
            print(dtime + ' no data ' + str(e))
            return False

        if host_type:
            addr_info = requests.get(wallet_host + '/newaddr')

            if addr_info.status_code == 200:
                info = addr_info.json()

            result = {
                "address": info['address'],
                "ip": "123.123.123.123"
            }

            return result
        else:
            return False


class TopUp(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('host')
        args = parser.parse_args()
        dtime = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
        try:
            host = args['host']
        except KeyError as e:
            print(dtime + ' no data' + str(e))
            return False

        if host:
            invoice_data = invoice(amount=0.01, cur='EUR', desc=host)

            id = invoice_data['id']
            bolt = invoice_data['payreq']
            register_webhook(id, wallet_host + '/chargify')

            result = {
                "invoice": bolt
            }

            return result
        else:
            return False


#e-mail or telegram id
api.add_resource(CreateVPS, '/create')
api.add_resource(TopUp, '/topup')

if __name__ == '__main__':
    app.run(debug=False, port=16444)