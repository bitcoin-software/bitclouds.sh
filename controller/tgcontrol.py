import telegram
import configparser

tg_config = configparser.ConfigParser()
tg_config.read('../controller/config.ini')

tg_token = tg_config['telegram']['token']

bot = telegram.Bot('TOKEN')

chat_id = tg_config['telegram']['admin_chatid']
