import pymongo
import datetime

dbclient = pymongo.MongoClient('localhost')
mongo_db = "hosting"
mongo = dbclient[mongo_db]


def find_hosts():
    hosts = mongo.hosts.find()

    if hosts:
        return hosts
    else:
        return False
