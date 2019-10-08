from flask import Flask
from flask_restful import Resource, Api, reqparse, request
import datetime
from btc_wallet import bstartd, bgetunused, bgetnew, bnotify
import configparser

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
            status = args['status']
            address = args['address']
        except KeyError as e:
            print(dtime + ' no data' + str(e))
            print(request.get_data())
            return False


class getnew(Resource):
    def get(self):
        dtime = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
        result = {
            "address": bgetnew(wallet)
        }
        return result


if __name__ == '__main__':
    wallet_list = [wallet]
    bstartd(wallet_list)

    ipn.add_resource(elify, '/elify')
    ipn.add_resource(getnew, '/newaddr')

    notifyURL = config['ipn']['url'] + '/elify'
    addr = bgetunused(wallet)
    print(addr)
    print(bnotify(wallet, addr, notifyURL))

    app.run(debug=False, port=16333)

