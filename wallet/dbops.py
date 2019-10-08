import pymongo
import datetime

dbclient = pymongo.MongoClient('localhost')
mongo_db = "hosting"
mongo = dbclient[mongo_db]


def find_host(address):
    ex_user = mongo.hosts.find_one({"address": address})

    if ex_user:
        return ex_user
    else:
        return False


def create_host(address):
    dtime = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')

    hostdata = {"created_date": dtime,
                "address": address,
                "status": "new",
                "balance": 0
                }

    recordID = mongo.hosts.insert_one(hostdata)


def subscribe_host(address, hours):
    mongo.hosts.update_one(
    {"address": address},
        {
            "$set":
                {
                    "status": "subscribed",
                    "balance": hours
                }
        }
    )


def add_tx(address, tx):
    dtime = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')

    hostdata = {"timestamp": dtime,
                "address": address,
                "tx": tx
                }

    recordID = mongo.hosts.insert_one(hostdata)
