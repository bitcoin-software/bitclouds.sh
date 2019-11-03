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


def create_host(address, plan="basic", image="debian"):
    dtime = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')

    hostdata = {"created_date": dtime,
                "address": address,
                "status": "new",
                "plan": plan,
                "image": image,
                "balance": 0
                }

    recordID = mongo.hosts.insert_one(hostdata)


def subscribe_host(address, hours):
    host = mongo.hosts.find_one({"address": address})
    balance = host['balance']

    mongo.hosts.update_one(
        {"address": address},
        {
            "$set":
                {
                    "status": "subscribed",
                    "balance": balance + hours
                }
        }
    )


def log_acc(address, record):
    host = mongo.hosts.find_one({"address": address})

    dtime = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
    if host:
        data = {"timestamp": dtime,
                "address": address,
                "record": record,
                "balance": host['balance']
                }

        recordID = mongo.logs.insert_one(data)


def find_tx(txhash):
    ex_tx = mongo.txs.find_one({"txhash": txhash})

    if ex_tx:
        return ex_tx
    else:
        return False


def add_tx(address, txhash, amount_sats, status='paid', chargeid='none', prev_outhash='none'):
    dtime = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')

    txdata = {"timestamp": dtime,
                "address": address,
                "amount": amount_sats,
                "txhash": txhash,
                "chargeid": chargeid,
                "prev_outhash": prev_outhash,
                "status": status
                }

    log_acc(address, status + " tx " + txhash)

    recordID = mongo.txs.insert_one(txdata)

    return recordID


def update_tx(address, txid, status):
    dtime = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')

    mongo.txs.update_one(
    {"txhash": txid, "address": address},
        {
            "$set":
                {
                    "status": status,
                    "last_update": dtime
                }
        }
    )

    log_acc(address, status + " tx " + txid)
