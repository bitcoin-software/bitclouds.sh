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


def check_paid(address):
    ex_tx = mongo.txs.find_one({"address": address})

    if ex_tx:
        return ex_tx
    else:
        return False

def get_notifiable():
    hosts = mongo.hosts.find({
        "status": "subscribed",
        "balance": {'$lt': 25},
        "webhook": {'$not': None}
    })

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

    _ = mongo.hetzner.insert_one(hostdata)
    return hostdata


def get_bitbsd(plan='bitcoind'):
    hosts = mongo.bitbsd.find({"plan": plan})

    if hosts:
        return hosts
    else:
        return False


def add_bitbsd(address, bitbsd_id, ipv4, ssh_port, rpc_port, rpc_authline, rpc_user, rpc_pwd, plan, pwd):
    dtime = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')

    hostdata = {"created_date": dtime,
                "address": address,
                "plan": plan,
                "id": bitbsd_id,
                "ipv4": ipv4,
                "ssh_port": ssh_port,
                "rpc_port": rpc_port,
                "rpc_user": rpc_user,
                "rpc_pwd": rpc_pwd,
                "rpc_authline": rpc_authline,
                "pwd": pwd
                }

    _ = mongo.bitbsd.insert_one(hostdata)
    return hostdata


def add_bitbsd_cln(address, bitbsd_id, ipv4, ssh_port, app_port, alias, rpc_user, rpc_pwd, plan, pwd):
    dtime = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')

    hostdata = {"created_date": dtime,
                "address": address,
                "plan": plan,
                "id": bitbsd_id,
                "ipv4": ipv4,
                "ssh_port": ssh_port,
                "app_port": app_port,
                "alias": alias,
                "rpc_user": rpc_user,
                "rpc_pwd": rpc_pwd,
                "pwd": pwd
                }

    _ = mongo.bitbsd.insert_one(hostdata)
    return hostdata


def add_bitbsd_rs(address, bitbsd_id, ipv4, ssh_port, app_port, plan, pwd):
    dtime = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')

    hostdata = {"created_date": dtime,
                "address": address,
                "plan": plan,
                "id": bitbsd_id,
                "ipv4": ipv4,
                "ssh_port": ssh_port,
                "app_port": app_port,
                "pwd": pwd
                }

    _ = mongo.bitbsd.insert_one(hostdata)
    return hostdata



