from flask import Flask
from flask_restful import Resource, Api, reqparse, request
from hashlib import blake2b
import requests
import datetime
import sys
import configparser

app = Flask(__name__)
api = Api(app)

api_config = configparser.ConfigParser()

api_config.read('../controller/config.ini')

wallet_host = api_config['wallet']['host']
project_path = api_config['paths']['local_path']
sys.path.insert(1, project_path + '/wallet')

# charge.py
#invoice(msat=None, amount=0, cur='EUR', desc=False)
#register_webhook(invoice_id, callback_url):
from charge import invoice, register_webhook
from ctrldbops import get_hetzner, find_hosts


class CreateVPS(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('image')
        args = parser.parse_args()
        dtime = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
        try:
            host_type = args['image']
        except KeyError as e:
            print(dtime + ' no data ' + str(e))
            return False

        if host_type:
            addr_info = requests.post(wallet_host + '/newaddr', data={"image": host_type})

            if addr_info.status_code == 200:
                info = addr_info.json()

            invoice_data = invoice(amount=0.03, cur='EUR', desc=info['address'])
            id = invoice_data['id']
            bolt = invoice_data['payreq']
            register_webhook(id, wallet_host + '/chargify')

            result = {
                "host": info['address'],
                "paytostart": bolt
            }

            return result
        else:
            return False


class Images(Resource):
    def get(self):
        dtime = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')

        result = {
            "images": ['debian', 'centos', 'ubuntu'] #'freebsd', 'bitcoind', 'lightningd'
        }

        return result


class Status(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('host')
        args = parser.parse_args()
        dtime = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')

        hosts = get_hetzner()

        try:
            addr = args['host']
            result = {
                "status": "wrong host"
            }
        except KeyError as e:
            return {"error": "need a host (btc addr)"}


        for host in hosts:
            if host['address'] == addr:
                result = {
                    "ip": host['ipv4'],
                    "pwd": host['pwd'],
                    "status": "subscribed"
                }

        accs = find_hosts()

        for acc in accs:
            if acc['address'] == addr:
                balance = acc['balance']
                image = acc['image']
                if (image == 'freebsd') or (image == 'bitcoind') or (image == 'lightningd'):
                    result['login_username'] = "bsd"
                if balance > 0:
                    result['hours_left'] = balance
                else:
                    result = {
                        "status": "pending payment"
                    }

        return result


class TopUp(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('host')
        parser.add_argument('sats')
        args = parser.parse_args()

        isamount = False

        host = args['host']
        if not host:
            return {"error": "provide host id (bitcoin address)"}

        sats = args['sats']

        try:
            if int(sats) > 0:
                isamount = True
            else:
                isamount = False
        except Exception as e:
            pass

        if host:
            if not isamount:
                invoice_data = invoice(amount=0.03, cur='EUR', desc=str(host))
                print("generating invoice for 0.03 EUR desc=" + host)
            elif isamount:
                print(sats)
                invoice_data = invoice(msat=sats*1000, desc=str(host))
                print("generating invoice for " + str(sats) + " sats desc=" + str(host))

            print(invoice_data)
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
api.add_resource(Images, '/images')
api.add_resource(Status, '/status')

if __name__ == '__main__':
    app.run(debug=False, port=16444)