import pymongo
import datetime

dbclient = pymongo.MongoClient('localhost')
mongo_db = "cloud"
mongo = dbclient[mongo_db]

dtime = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')


def find_hosts():
    hosts = mongo.hosts.find()

    if hosts:
        return hosts
    else:
        return False


def find_host(address):
    ex_user = mongo.hosts.find_one({"address": address})

    if ex_user:
        return ex_user
    else:
        return False


def add_host(name, ipv4, pwd, plan="1sat"):
    dtime = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')

    hostdata = {"created_date": dtime,
                "name": name,
                "plan": plan,
                "ipv4": ipv4,
                "pwd": pwd,
                "status": "pending"
                }

    _ = mongo.hetzner.insert_one(hostdata)
    return hostdata

