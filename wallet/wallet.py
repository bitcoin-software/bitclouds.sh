from flask import Flask
from flask_restful import Resource, Api, reqparse, request
import datetime
from btc_wallet import bstartd, bgetunused, bgetnew, bnotify, bstopd, blistunspent
import configparser
from charge import get_invoice
from dbops import find_host, create_host, subscribe_host, add_tx, find_tx, update_tx
import sys

wallet_config = configparser.ConfigParser()
wallet_config.read('config.ini')

wallet = wallet_config['electrum']['wallet']

app = Flask(__name__)
ipn = Api(app)

api_config = configparser.ConfigParser()
api_config.read('../controller/config.ini')
project_path = api_config['paths']['local_path']
sys.path.insert(1, project_path + '/controller')
from orchestrator import new_server

def convert_sats2hours(address, sats):
        hours = int(sats / 66) - 1
        if hours < 0:
            hours = 0

        return hours


class elify(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('address')
        parser.add_argument('status')
        args = parser.parse_args()
        dtime = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
        try:
            status = '['+str(args['status'])+']'
            address = '['+str(args['address'])+']'
        except KeyError as e:
            print(dtime + ' no data' + str(e))
            print(request.get_data())
            return False

        print(dtime + " new status " + status + " for " + address)
        if status is not '':
            unspents = blistunspent(wallet)
        #print(unspents)
            for unspent in unspents:
                if address == unspent['address']:
                    amount_sats = unspent['value']*100000000
                    outhash = status
                    prev_outhash = unspent['prevout_hash']
                    if unspent['height'] == 0:
                        if not find_tx(outhash):
                            add_tx(address=address, txhash=outhash, amount_sats=amount_sats, status='paid', chargeid='none', prev_outhash=prev_outhash)
                        else:
                            print(dtime + 'tx already exists')
                    elif unspent['height'] > 0:
                        existing_tx = find_tx(outhash)
                        if existing_tx:
                            if existing_tx['status'] == 'paid':

                                new_host = find_host(address)
                                if new_host:
                                    if new_host['status'] == 'new':
                                        serverData = new_server(address)

                                update_tx(address, outhash, 'confirmed')
                                hours = convert_sats2hours(address, amount_sats)
                                subscribe_host(address, hours)
                                print("\n\n" + str(find_host(address)) + "\n\n")
                            else:
                                print(dtime + ' ' + outhash + 'tx already confirmed')
                        else:
                            print(dtime + ' ' + outhash + ' tx not found but confirmed')

        return True


class chargify(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id')
        args = parser.parse_args()
        dtime = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
        try:
            id = args['id']
        except KeyError as e:
            print(dtime + ': error on handling callback from charge - ' + str(e))
            return False
        invoice_data = get_invoice(id=id)
        #print(invoice_data)
        address = invoice_data['description']
        status = invoice_data['status']
        amount_sats = int(int(invoice_data['msatoshi'])/1000)
        bolt = invoice_data['payreq']
        print(dtime + " new status [" + status + "] for [" + id + "]")
        if status == 'paid':
            new_host = find_host(address)
            if new_host:
                if new_host['status'] == 'new':
                    serverData = new_server(address)
            add_tx(address=address, txhash=bolt, amount_sats=amount_sats, status='confirmed', chargeid=id,
                   prev_outhash='none')
            hours = convert_sats2hours(address, amount_sats)
            subscribe_host(address, hours)
        print("\n\n" + str(find_host(address)) + "\n\n")
        return True


class getnew(Resource):
    def post(self):
        dtime = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
        address = str(bgetunused(wallet).rstrip())
        parser = reqparse.RequestParser()
        parser.add_argument('image')
        args = parser.parse_args()
        image = args['image']
        if find_host(address):
            print('unused addr: ' + address)
            address = str(bgetnew(wallet).rstrip())
        else:
            pass

        result = {
            "address": address
        }
        print(dtime)
        print("new addr:" + address + ";\nwill notify:" + notifyURL + ";\n")
        bnotify(wallet, address, notifyURL)
        create_host(address, "basic", )
        return result


if __name__ == '__main__':
    wallet_list = [wallet]
    bstopd()
    bstartd(wallet_list)

    ipn.add_resource(elify, '/elify')
    ipn.add_resource(chargify, '/chargify')
    ipn.add_resource(getnew, '/newaddr')

    notifyURL = wallet_config['ipn']['url'] + '/elify'
    addr = bgetunused(wallet)

    app.run(debug=False, port=16333)

