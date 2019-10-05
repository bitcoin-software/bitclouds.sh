from flask import Flask
from flask_restful import Resource, Api, reqparse, request
from hashlib import blake2b
import datetime

app = Flask(__name__)
api = Api(app)


class CreateAccount(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('login')
        parser.add_argument('password')
        args = parser.parse_args()
        dtime = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
        try:
            login = args['login']
            pwd = args['password']
        except KeyError as e:
            print(dtime + ' no login or pwd ' + str(e))
            return False

        token=blake2b(pwd).hexdigest()

        result = {
            "token": token
        }

        return result


class LoginAccount(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('login')
        parser.add_argument('password')
        args = parser.parse_args()
        dtime = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
        try:
            login = args['login']
            pwd = args['password']
        except KeyError as e:
            print(dtime + ' no login or pwd' + str(e))
            return False

        def checkLogin(lgn, pwd):
            if lgn == "test" and pwd == "test":
                return True
            else:
                return False

        if checkLogin(login, pwd):
            token = blake2b(pwd).hexdigest()
        else:
            return False

        result = {
            "token": token
        }

        return result


class CreateCloud(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name')
        parser.add_argument('token')
        args = parser.parse_args()
        dtime = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
        try:
            token = args['token']
            name = args['name']
        except KeyError as e:
            print(dtime + ' no data' + str(e))
            return False

        if token == blake2b(b"test").hexdigest():
            result = {
                "id": "1ABCdef"
            }

            return result
        else:
            return False


class CreateVPS(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name')
        parser.add_argument('cloudid')
        parser.add_argument('token')
        args = parser.parse_args()
        dtime = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
        try:
            token = args['token']
            name = args['name']
            cloudid = args['cloudid']
        except KeyError as e:
            print(dtime + ' no data' + str(e))
            return False

        if token == blake2b(b"test").hexdigest():

            result = {
                "id": "1ABCdef",
                "ip": "123.123.123.123"
            }

            return result
        else:
            return False


class GetAccountClouds(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('token')
        args = parser.parse_args()
        dtime = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
        try:
            token = args['token']
        except KeyError as e:
            print(dtime + ' no data' + str(e))
            return False

        if token == blake2b(b"test").hexdigest():
            result = {
                "work": {
                    "id": "345ssfwer234ewraded234dw3frdwrff3ae",
                    "vps_list": [{"type": "freebsd", "id": "45fe4fe45fe45fe45fe45fw4f4wf"}, {"type": "debian", "id": "e4gftde53dw4g4wdwgf"}]
                },
                "home": {
                    "id": "aded234dw3frdwrff3ae345ssfwer234ewr",
                    "vps_list": [{"type": "centos", "id": "l67ut67jur65fe45fe45fw4f4wf"},
                                 {"type": "debian", "id": "o9uojj3dwrfa43r3w4a3s4fa"}]
                }
            }

            return result
        else:
            return False


#e-mail or telegram id
api.add_resource(CreateAccount, '/create-acc')
api.add_resource(LoginAccount, '/login-acc')
api.add_resource(CreateCloud, '/create-cloud')
api.add_resource(CreateVPS, '/create-vps')
api.add_resource(GetAccountClouds, '/acc-clouds')

if __name__ == '__main__':
    app.run(debug=False, port=16444)