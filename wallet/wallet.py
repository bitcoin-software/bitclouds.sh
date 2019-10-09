from flask import Flask
from flask_restful import Resource, Api, reqparse, request
import datetime
from btc_wallet import bstartd, bgetunused, bgetnew, bnotify, bstopd, blistunspent
import configparser
from charge import get_invoice
from dbops import create_host, subscribe_host, add_tx

config = configparser.ConfigParser()
config.read('config.ini')

wallet = config['electrum']['wallet']

app = Flask(__name__)
ipn = Api(app)


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
            add_tx(address, status)
        unspents = blistunspent(wallet)
        print(unspents)

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
        print(invoice_data)
        description = invoice_data['description']
        print(dtime + " new status [" + invoice_data['status'] + "] for [" + invoice_data['id'] + "]")

        return True


class getnew(Resource):
    def get(self):
        dtime = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
        address = str(bgetunused(wallet).rstrip())
        result = {
            "address": address
        }
        print(dtime)
        print("new addr:" + address + ";\nwill notify:" + notifyURL + ";\n")
        bnotify(wallet, address, notifyURL)
        create_host(address)
        return result


if __name__ == '__main__':
    wallet_list = [wallet]
    bstopd()
    bstartd(wallet_list)

    ipn.add_resource(elify, '/elify')
    ipn.add_resource(chargify, '/chargify')
    ipn.add_resource(getnew, '/newaddr')

    notifyURL = config['ipn']['url'] + '/elify'
    addr = bgetunused(wallet)

    app.run(debug=False, port=16333)

