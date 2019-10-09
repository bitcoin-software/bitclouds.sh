import pymongo
import json
import sys

dbclient = pymongo.MongoClient('localhost')
mongo_db = "hosting"
mongo = dbclient[mongo_db]

hosts = mongo.hosts.find()

txs = mongo.txs.find()


hetzners = mongo.hetzner.find()


arg = sys.argv[1]

if arg == 'list':
    for host in hosts:
        print(host)

    for tx in txs:
        print(tx)

    for server in hetzners:
        print(server)

elif arg == 'del':
    dbclient.drop_database(mongo_db)

