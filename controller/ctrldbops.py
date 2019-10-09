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


def get_suspended():
    hosts = mongo.hosts.find({"status": "suspended"})

    if hosts:
        return hosts
    else:
        return False


def delete_host(address):
    host = mongo.hosts.find_one({"address": address})

    mongo.hosts.update_one(
        {"address": address},
        {
            "$set":
                {
                    "status": "deleted",
                }
        }
    )


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
                        "balance": balance - 1
                    }
            }
        )
    elif status == "subscribed":
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


def get_hetzner():
    hosts = mongo.hetzner.find()

    if hosts:
        return hosts
    else:
        return False


def add_hetzner(address, hetzner_id, ipv4, plan, pwd):
    dtime = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')

    hostdata = {"created_date": dtime,
                "address": address,
                "plan": plan,
                "id": hetzner_id,
                "ipv4": ipv4,
                "pwd": pwd
                }

    recordID = mongo.hetzner.insert_one(hostdata)


