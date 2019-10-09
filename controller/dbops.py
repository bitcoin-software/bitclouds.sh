import pymongo
import datetime

dbclient = pymongo.MongoClient('localhost')
mongo_db = "hosting"
mongo = dbclient[mongo_db]

dtime = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')


def find_hosts():
    hosts = mongo.hosts.find()

    if hosts:
        return hosts
    else:
        return False


def deduct_host(address):
    host = mongo.hosts.find_one({"address": address})
    balance = host['balance']
    status = host['status']

    if ((balance - 1) > 0) and (status == "subscribed"):
        mongo.hosts.update_one(
            {"address": address},
            {
                "$set":
                    {
                        "status": "subscribed",
                        "balance": balance - 1
                    }
            }
        )
    else:
        mongo.hosts.update_one(
            {"address": address},
            {
                "$set":
                    {
                        "status": "suspended",
                        "balance": 0
                    }
            }
        )