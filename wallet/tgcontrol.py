#from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, RegexHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
import telegram
import time

import configparser

tg_config = configparser.ConfigParser()
tg_config.read('../wallet/config.ini')

tg_token = tg_config['telegram']['token']

bot = telegram.Bot('TOKEN')

chat_id = tg_config['telegram']['admin_chatid']


def ticket_notify(premium, address, contact, msg):
    if premium == '*':
        header = "\n <b>$$$ PREMIUM $$$</b> \n"
        gold = True
    else:
        header = ""
        gold = False

    reminded = 0
    while reminded < 3:
        if gold:
            reminded += 1
        else:
            reminded = 100
        bot.send_message(chat_id=chat_id, text=header + 'Support request for <b>' + address +
                                              '</b>\n' + contact + '\n--- START ---\n<i>' + msg +
                                              '</i>\n--- END ---'
                         , parse_mode=ParseMode.HTML)
        header = 'reminder:\n'
        time.sleep(22000)
