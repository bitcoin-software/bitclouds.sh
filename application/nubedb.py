import datetime
import pymongo

dbclient = pymongo.MongoClient('localhost')
mongo_db = "nube"
mongo = dbclient[mongo_db]


def find_keys():
    hosts = mongo.keys.find()

    if hosts:
        return hosts
    else:
        return False


def get_keydata(keyid):
    ex_user = mongo.keys.find_one({"cid": keyid})

    if ex_user:
        return ex_user
    else:
        return False


def add_key(keyid):
    dtime = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')

    keydata = {
        "created_date": dtime,
        "cid": keyid,
        "status": "subscribed",
        "balance": 9
    }

    if not get_keydata(keyid):
        _ = mongo.keys.insert_one(keydata)
    return keydata


def subscribe_key(keyid, sats):
    keydata = mongo.keys.find_one({"cid": keyid})
    balance = keydata['balance']

    mongo.keys.update_one(
        {"cid": keyid},
        {
            "$set":
                {
                    "status": "subscribed",
                    "balance": balance + sats
                }
        }
    )


def deactivate_key(keyid):
    keydata = mongo.keys.find_one({"cid": keyid})
    if keydata:
        mongo.keys.update_one(
            {"cid": keyid},
            {
                "$set":
                    {
                        "status": "inactive",
                        "balance": 0
                    }
            }
        )


