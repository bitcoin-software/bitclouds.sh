from flask import Flask
from flask_restful import Resource, Api, reqparse, request
from hashlib import blake2b
import requests
import datetime

app = Flask(__name__)
api = Api(app)

wallet_host = "http://10.10.0.7:16333"

class CreateVPS(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('type')
        args = parser.parse_args()
        dtime = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
        try:
            type = args['type']
        except KeyError as e:
            print(dtime + ' no data' + str(e))
            return False

        if type:
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

#e-mail or telegram id
api.add_resource(CreateVPS, '/create')

if __name__ == '__main__':
    app.run(debug=False, port=16444)