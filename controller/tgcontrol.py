import telegram
import configparser

tg_config = configparser.ConfigParser()
tg_config.read('../controller/config.ini')

tg_token = tg_config['telegram']['token']

bot = telegram.Bot('TOKEN')

chat_id = tg_config['telegram']['admin_chatid']

bot.send_message(chat_id=admin_chat, text='swapBot: ' + msg)

bot.send_message(chat_id=userid, text='<b>Lightning wallets</b>:\n' +
                                      '<a href="https://www.walletofsatoshi.com/">Wallet of Satoshi</a>\n' +
                                      '<a href="https://bluewallet.io/">BlueWallet</a>'
                 , parse_mode=ParseMode.HTML)
