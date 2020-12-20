import requests
import os


def notify(bot_message):

    def tgsend():
        tg_bot_token = os.environ['TG_TOKEN']
        tg_bot_chatID = os.environ['TG_CHAT']
        send_text = 'https://api.telegram.org/bot' + tg_bot_token + '/sendMessage?chat_id=' + \
                    tg_bot_chatID + '&parse_mode=Markdown&text=' + bot_message
        try:
            response = requests.get(send_text, timeout=3)
            if response.status_code == 200:
                msgsent = True
            else:
                msgsent = False
        except Exception as e_tg:
            print('telegram send error')
            print(e_tg)
            msgsent = False

        return msgsent

    try:
        headers = {
            'Content-Type': 'application/json',
        }

        data = '{"text": "' + bot_message + '"}'

        response = requests.post(os.environ['MSG_ENDPOINT'] + '/msg',
                                 headers=headers, data=data, verify=False, timeout=9)

        if response.status_code == 200:
            sent = True
        else:
            sent = tgsend()
    except Exception as e:
        print('matrix sent error')
        print(e)
        sent = tgsend()

    return sent

