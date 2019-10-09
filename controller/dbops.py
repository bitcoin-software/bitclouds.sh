import pymongo
import datetime

dbclient = pymongo.MongoClient('localhost')
mongo_db = "hosting"
mongo = dbclient[mongo_db]

dtime = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')


def find_host(address):
    ex_user = mongo.hosts.find_one({"address": address})

    if ex_user:
        return ex_user
    else:
        return False


