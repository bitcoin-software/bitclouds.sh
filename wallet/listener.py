dbclient = pymongo.MongoClient('localhost')
mongo_db = "hosting"
mongo = dbclient[mongo_db]

hosts = mongo.hosts.find()

txs = mongo.txs.find()

print(hosts)
print(txs)
