import pymongo
import datetime
import os


dbclient = pymongo.MongoClient('localhost')
mongo_db = "bitclouds"
mongo = dbclient[mongo_db]


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


def find_ips():
    ips = mongo.ips.find()

    if ips:
        return ips
    else:
        return False


def bind_ip(name, ip):
    mongo.ips.update_one(
        {"ip4": ip},
        {
            "$set":
                {
                    "status": name
                }
        }
    )


def get_wan_address(name):
    ip = mongo.ips.find_one({"status": name})

    return ip


def get_free_wan():
    ip = mongo.ips.find_one({"status": "free"})

    if ip:
        return ip['ip4']
    else:
        return False


def free_ip(ip):
    ip = mongo.ips.find_one({"ip4": ip})

    mongo.ips.update_one(
        {"ip4": ip},
        {
            "$set":
                {
                    "status": "free"
                }
        }
    )


def add_host(name, ipv4, pwd, status, image, username='user'):
    os.system('ssh-keygen -f /tmp/' + name + '.key -t ed25519 -N ""')

    prv_keyfile = '/tmp/' + name + '.key'
    pub_keyfile = '/tmp/' + name + '.key.pub'

    with open(prv_keyfile, 'r') as file:
        prv_key = file.read()

    with open(pub_keyfile, 'r') as file:
        pub_key = file.read()

    os.remove(prv_keyfile)
    os.remove(pub_keyfile)

    dtime = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')

    hostdata = {"created_date": dtime,
                "name": name,
                "balance": 0,
                "image": image,
                "username": username,
                "pwd": pwd,
                "status": status,
                "init_pub": pub_key.replace('\n', ''),
                "init_priv": prv_key,
                "key_requested": False
                }

    _ = mongo.cloud.insert_one(hostdata)
    return hostdata


def init_host(name, lan_ip, wan_ip):
    mongo.cloud.update_one(
        {"name": name},
        {
            "$set":
                {
                    "status": "init",
                    "lan_ip": lan_ip,
                    "wan_ip": wan_ip
                }
        }
    )


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

    free_ip(host['wan_ip'])


def register_payment(name, invoice, status, ip):
    dtime = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')

    txdata = {
        "name": name,
        "timestamp": dtime,
        "invoice": invoice,
        "status": status,
        "from": ip
    }

    _ = mongo.payments.insert_one(txdata)


def hide_key(name):
    dtime = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
    mongo.cloud.update_one(
        {"name": name},
        {
            "$set":
                {
                    "key_requested": dtime
                }
        }
    )
