import requests
import datetime

import configparser

config = configparser.ConfigParser()
config.read('config.ini')

#invoice_info_request = requests.post('https://charge.ysx.in/', data={"bolt": plain_invoice},
#                                     auth=('api-token', 'eih4veijichaiya1oh3aeS3fa4ieb8'))

charge_url = config['charge']['url']
charge_token = config['charge']['token']


def getinfo():
    node_info_request = requests.get(charge_url + '/info', auth=('api-token', charge_token))

    if node_info_request.status_code == 200:
        node_info = node_info_request.json()
        try:
            #invoice_id = invoice_info['payment_hash']
            # print('sms id: ' + invoice_id)
            # print('info: \n' + str(invoice_info))
            pass
        except KeyError as e:
            print('key error')
        return node_info
    else:
        return False


def invoice(msat=None, amount=0, cur='EUR', desc=False):

    dtime = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')

    if not desc:
        desc=dtime+'-invoice-without-description'

    crypto = {
        'msatoshi': msat,
        'description': desc,
        'expiry': 600
    }


    fiat = {
        'amount': amount,
        'currency': cur,
        'description': desc,
        'expiry': 600
    }

    if amount == 0:
        payload = crypto
    else:
        payload = fiat

    invoice_info_request = requests.post(charge_url + '/invoice', auth=('api-token', charge_token), data=payload)

    if invoice_info_request.status_code == 201:
        invoice_info = invoice_info_request.json()
        return invoice_info
        #will return
        #{'id': '_u_QrwUEVgAWjzClTGfll', 'msatoshi': '12682266', 'description': '2019-06-16 02:30:52-invoice-without-description', 'quoted_currency': 'EUR', 'quoted_amount': '1', 'rhash': '2efae1b2c46be1afb39487a07f4b87971606b1b3fe7995ebce2fe3bcfcb9db70', 'payreq': 'lnbc126822660p1pws2ladpp59mawrvkyd0s6lvu5s7s87ju8jutqdvdnleuet67w9l3mel9emdcqdzvxgcrzwfdxqmz6vfkyqcryw3nxqar2v3dd9h8vmmfvdjj6amfw35x7at594jx2umrwf5hqarfdahqxqyjw5qcqp2rzjqwgtt4zf9hp02vvw2ge6kt8t7m2gj9ygrge7765ud0xmkse6mxrdqzxjkyqqw4cqqqqqqqqqqqqqrssqrcy5e2zdrnnkfphhewf0d6548fp2xam9ax2vkuy4j2nqwnlx2rnlk4pd7lx2sy9e3fpjym2ahc3pyjqeuxnran6hg2mjkmz7t3v6krzmgqgud0nc', 'expires_at': 1561246253, 'created_at': 1560641453, 'metadata': None, 'status': 'unpaid'}
    else:
        print('error: ' + str(invoice_info_request.status_code))
        return False


def get_invoice(id=None):
    if id:
        data = requests.get(charge_url + '/invoice/'+id,
                                             auth=('api-token', charge_token))
    else:
        data = requests.get(charge_url + '/invoices',
                                            auth=('api-token', charge_token))

    if data.status_code == 200:
        invoice_info = data.json()
        return invoice_info
    else:
        return False


def register_webhook(invoice_id, callback_url):
    payload = {
        'url': callback_url
    }

    webhook_info_request = requests.post(charge_url + '/invoice/'+invoice_id+'/webhook',
                                         auth=('api-token', charge_token), data=payload)

    if webhook_info_request.status_code == 201:
        return True
    elif webhook_info_request.status_code == 405:
        print('already paid')
        return False
    elif webhook_info_request.status_code == 410:
        print('invoice expired')
        return False

    return False


