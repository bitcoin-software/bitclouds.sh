import pymongo
import datetime

dbclient = pymongo.MongoClient('localhost')
mongo_db = "cloud"
mongo = dbclient[mongo_db]

dtime = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')


def find_hosts():
    hosts = mongo.cloud.find()

    if hosts:
        return hosts
    else:
        return False


def get_hostdata(name):
    ex_user = mongo.cloud.find_one({"name": name})

    if ex_user:
        return ex_user
    else:
        return False


def add_host(name, ipv4, pwd, status, image):
    dtime = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')

    hostdata = {"created_date": dtime,
                "name": name,
                "balance": 0,
                "image": image,
                "ipv4": ipv4,
                "pwd": pwd,
                "status": status
                }

    _ = mongo.cloud.insert_one(hostdata)
    return hostdata


def subscribe_host(name, sats):
    host = mongo.cloud.find_one({"name": name})
    balance = host['balance']

    mongo.cloud.update_one(
        {"name": name},
        {
            "$set":
                {
                    "status": "subscribed",
                    "balance": balance + sats
                }
        }
    )


def deactivate_host(name):
    host = mongo.cloud.find_one({"name": name})
    balance = host['balance']

    mongo.cloud.update_one(
        {"name": name},
        {
            "$set":
                {
                    "status": "inactive",
                    "balance": 0
                }
        }
    )
