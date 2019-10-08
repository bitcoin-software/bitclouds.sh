from flask import Flask
from flask_restful import Resource, Api, reqparse, request
import datetime
from btc_wallet import bstartd, bgetunused, bgetnew, bnotify
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

app = Flask(__name__)
ipn = Api(app)


class elify(Resource):
    def post(self):
        #parser = reqparse.RequestParser()
        #parser.add_argument('token')
        #args = parser.parse_args()
        #dtime = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
        #try:
        #    token = args['token']
        #except KeyError as e:
        #    print(dtime + ' no data' + str(e))
        #    return False

        print(str(request.data))


if __name__ == '__main__':
    wallet = config['electrum']['wallet']
    wallet_list = [wallet]
    bstartd(wallet_list)

    ipn.add_resource(elify, '/elify')

    notifyURL = config['ipn']['url'] + '/elify'
    print(bgetunused(wallet))
    print(bnotify(wallet, 'addr', notifyURL))

    app.run(debug=False, port=16333)

