import pymongo
import datetime

dbclient = pymongo.MongoClient('localhost')
mongo_db = "tipdb"
mongo = dbclient[mongo_db]

dtime = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')


def find_user():
    ex_user = mongo.users.find_one({"platform": platform, "user": userid})

    if ex_user:
        return ex_user
    else:
        return False


def create_user():
    userdata = {"created_date": dtime,
                "platform": 'telegram',
                "userhash": userhash,
                "balance": 0,
                "user": userid
                }
    recordID = mongo.users.insert_one(userdata)
