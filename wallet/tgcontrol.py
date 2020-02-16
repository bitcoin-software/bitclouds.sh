#from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, RegexHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
import telegram
import time

from common import config

tg_token = config['telegram']['token']
chat_id = config['telegram']['admin_chatid']

if tg_token and chat_id:
    bot = telegram.Bot(tg_token)

    def ticket_notify(premium, address, contact, msg):
        if premium == '$':
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
else:
    def ticket_notify(*args, **kwargs): pass
