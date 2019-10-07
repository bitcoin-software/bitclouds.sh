from bitcart.coins.btc import BTC
import configparser

config = configparser.ConfigParser()
config.read('config.ini')


btc = BTC(xpub=str(config['electrum']['xpub']))


@btc.on("new_transaction")
def callback_func(event, tx):
    print(event)
    print(tx)


btc.poll_updates()