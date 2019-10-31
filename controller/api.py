from flask import Flask, jsonify
import requests
import sys
import configparser

app = Flask(__name__)

app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.url_map.strict_slashes = False

api_config = configparser.ConfigParser()
api_config.read('../controller/config.ini')

wallet_host = api_config['wallet']['host']
project_path = api_config['paths']['local_path']
sys.path.insert(1, project_path + '/wallet')

# charge.py
#invoice(msat=None, amount=0, cur='EUR', desc=False)
#register_webhook(invoice_id, callback_url):
from charge import invoice, register_webhook
from ctrldbops import get_hetzner, find_hosts, get_bitbsd


@app.route('/create/<image>')
def create_vps(image):
    addr_info = requests.post(wallet_host + '/newaddr', data={"image": image})
    if addr_info.status_code != 200:
        return
    
    info = addr_info.json()
    invoice_data = invoice(amount=0.03, cur='EUR', desc=info['address'])
    id = invoice_data['id']
    bolt = invoice_data['payreq']
    register_webhook(id, wallet_host + '/chargify')

    result = {
        "host": info['address'],
        "paytostart": bolt
    }

    return jsonify(result)


@app.route('/images')
def images():
    result = {
        "images": ['debian', 'centos', 'ubuntu'] #'freebsd', 'bitcoind', 'lightningd'
    }

    return jsonify(result)

@app.route('/status/<host>')
def status(host):
    print('xyz')
    hetz_hosts = get_hetzner()
    bit_hosts = get_bitbsd()

    for hh in hetz_hosts:
        if hh['address'] == host:
            result = {
                "ip": hh['ipv4'],
                "pwd": hh['pwd'],
                "status": "subscribed"
            }

    for bh in bit_hosts:
        if bh['address'] == host:
            result = {
                "ip": 'bitbsd.org',
                "ssh_pwd": bh['pwd'],
                "ssh_usr": 'bitcoin',
                "rpc_user": bh['rpc_user'],
                "rpc_pwd": bh['rpc_pwd'],
                "rpc_port": bh['rpc_port'],
                "ssh_port": bh['ssh_port']
            }


    accs = find_hosts()

    for acc in accs:
        if acc['address'] == host:
            balance = acc['balance']
            image = acc['image']
            if (image == 'freebsd') or (image == 'bitcoind') or (image == 'lightningd'):
                result['login_username'] = "bsd"
            if balance > 0:
                result['hours_left'] = balance
            else:
                result = {
                    "status": "pending payment"
                }

    return result


@app.route('/topup/<host>', defaults={'sats': 0})
@app.route('/topup/<host>/<int:sats>')
def topup(host, sats):
    if sats == 0:
        invoice_data = invoice(amount=0.03, cur='EUR', desc=str(host))
        print("generating invoice for 0.03 EUR desc=" + host)
    else:
        print(sats)
        invoice_data = invoice(msat=int(sats)*1000, desc=str(host))
        print("generating invoice for " + str(sats) + " sats desc=" + str(host))

    print(invoice_data)
    id = invoice_data['id']
    bolt = invoice_data['payreq']
    register_webhook(id, wallet_host + '/chargify')

    result = {
        "invoice": bolt
    }

    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=False, port=16444)
