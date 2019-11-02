from flask import Flask, jsonify
import requests
import sys
import configparser
import threading
import time
import datetime

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
from ctrldbops import get_hetzner, find_hosts, get_bitbsd, check_paid, deduct_host, get_suspended, delete_host
from orchestrator import del_server


def accountant():
    threading.Timer(60.0, accountant).start()

    hosts = find_hosts()
    for host in hosts:
        if host['status'] == 'subscribed':
            print(host)
            deduct_host(host['address'])
            dtime = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
            print(dtime + ": " + host['address'] + "is subscribed; balance: " + str(
                host['balance']) + "' >> /tmp/acc.log")
        last = host['address']

    for host in get_suspended():
        print('deleting ' + host['address'])
        del_server(host['address'])
        delete_host(host['address'])
        time.sleep(5)


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
        "images": ['debian', 'centos', 'ubuntu', 'bitcoind', 'lightningd', 'rootshell'] #'freebsd', 'bitcoind', 'lightningd'
    }

    return jsonify(result)

@app.route('/status/<host>')
def status(host):
    print('xyz')
    hetz_hosts = get_hetzner()
    bit_hosts = get_bitbsd()
    cln_hosts = get_bitbsd('lightningd')
    rs_hosts = get_bitbsd('rootshell')

    result = dict()

    for hh in hetz_hosts:
        if hh['address'] == host:
            result = {
                "ip": hh['ipv4'],
                "pwd": hh['pwd']
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

    for bh in cln_hosts:
        if bh['address'] == host:
            result = {
                "ip": 'bitbsd.org',
                "ssh_pwd": bh['pwd'],
                "ssh_usr": 'lightning',
                "ssh_port": bh['ssh_port'],
                "app_port": bh['app_port'],
                "ssh2onion": "you can ssh directly to your .onion (/home/lightning/onion.domain) on port 22"
            }

    for bh in rs_hosts:
        if bh['address'] == host:
            result = {
                "ip": 'bitbsd.org',
                "ssh_pwd": bh['pwd'],
                "ssh_usr": 'satoshi',
                "ssh_port": bh['ssh_port'],
                "app_port": bh['app_port']
            }


    accs = find_hosts()

    for acc in accs:
        if acc['address'] == host:
            balance = acc['balance']
            image = acc['image']
            result['status'] = acc['status']
            if balance > 0:
                result['hours_left'] = balance
            else:
                result = {
                    "status": "awaiting payment! if you paid already wait until your instance is created."
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

accountant()

if __name__ == '__main__':
    app.run(debug=False, port=16444)
