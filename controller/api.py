from flask import Flask
from flask_restful import Resource, Api
import requests
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
from ctrldbops import get_hetzner, find_hosts, get_bitbsd


class CreateVPS(Resource):
    def get(self, image):
        addr_info = requests.post(wallet_host + '/newaddr', data={"image": image})
        if addr_info.status_code != 200:
            return
        
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


class Images(Resource):
    def get(self):
        result = {
            "images": ['debian', 'centos', 'ubuntu'] #'freebsd', 'bitcoind', 'lightningd'
        }

        return result


class Status(Resource):
    def get(self, host):
        hetz_hosts = get_hetzner()
        bit_hosts = get_bitbsd()

        for hh in hetz_hosts:
            if hh['address'] == host:
                result = {
                    "ip": host['ipv4'],
                    "pwd": host['pwd'],
                    "status": "subscribed"
                }

        for bh in bit_hosts:
            if bh['address'] == host:
                result = {
                    "ip": 'bitbsd.org',
                    "ssh_pwd": host['pwd'],
                    "ssh_usr": 'bitcoin',
                    "rpc_user": host['rpc_user'],
                    "rpc_pwd": host['rpc_pwd'],
                    "rpc_port": host['rpc_port'],
                    "ssh_port": host['ssh_port']
                }


        accs = find_hosts()

        for acc in accs:
            if acc['address'] == host:
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
    def get(self, host, sats):
        try:
            if int(sats) > 0:
                isamount = True
            else:
                isamount = False
        except Exception:
            isamount = False

        if host:
            if not isamount:
                invoice_data = invoice(amount=0.03, cur='EUR', desc=str(host))
                print("generating invoice for 0.03 EUR desc=" + host)
            elif isamount:
                print(sats)
                invoice_data = invoice(msat=int(sats)*1000, desc=str(host))
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
api.add_resource(Images, '/images')
api.add_resource(CreateVPS, '/create/<string:image>')
api.add_resource(TopUp, '/<string:host>/topup/<int:sats>')
api.add_resource(Status, '/<string:host>/status')

if __name__ == '__main__':
    app.run(debug=False, port=16444)
