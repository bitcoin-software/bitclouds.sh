from flask import Flask, jsonify
import requests
import sys
import threading
import time
import os
import datetime

app = Flask(__name__)

app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.url_map.strict_slashes = False


@app.route('/create/<image>')
def create_vps(image):
    if image in ['ubuntu']:
        addr_info = requests.post(wallet_host + '/newaddr', data={"image": image})
        if addr_info.status_code != 200:
            return addr_info.status_code
        info = addr_info.json()
        desc = 'BitClouds.sh: ' + info['address']
        invoice_data = invoice(amount=0.00000420, cur='BTC', desc=desc)
        id = invoice_data['id']
        bolt = invoice_data['payreq']
        register_webhook(id, wallet_host + '/chargify')

        result = {
            "host": info['address'],
            "paytostart": bolt
        }

        return jsonify(result)
    else:
        return {'error': 'no such image'}


@app.route('/images')
def images():
    result = {
        "images": ['ubuntu'] #'freebsd', 'bitcoind', 'lightningd'
    }

    return jsonify(result)


@app.route('/chkinv/<inv>')
def chkinv(inv):
    all_invoices = get_invoice()
    for local_invoice in all_invoices:
        if local_invoice['payreq'] == inv:
            return jsonify(local_invoice)
    return False


@app.route('/support/<address>/<string:contact>/<string:msg>', defaults={'premium': 'regular'})
@app.route('/support/<address>/<string:contact>/<string:msg>/<string:premium>')
def support(address, contact, msg, premium):
    if len(msg) > 300:
        formatted_msg = msg[:300]
    else:
        formatted_msg = msg
    if premium == 'urgent':
        desc = '$[support BitClouds.sh] | ' + address + ' | ' + contact + ':~ ' + formatted_msg
        invoice_data = invoice(amount=0.00009999, cur='BTC', desc=desc)
    elif premium == 'regular':
        desc = '*[support BitClouds.sh] | ' + address + ' | ' + contact + ':~ ' + formatted_msg
        invoice_data = invoice(amount=0.00000099, cur='BTC', desc=desc)

    id = invoice_data['id']
    bolt = invoice_data['payreq']
    register_webhook(id, wallet_host + '/support')

    result = {
        "paytosend": bolt
    }
    return jsonify(result)


@app.route('/status/<host>')
def status(host):
    hetz_hosts = get_hetzner()
    bit_hosts = get_bitbsd()
    cln_hosts = get_bitbsd('lightningd')
    rs_hosts = get_bitbsd('rootshell')
    p2e_hosts = get_bitbsd('pay2exec')

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
                "ip": 'bitclouds.link',
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
                "ip": 'bitclouds.link',
                "ssh_pwd": bh['pwd'],
                "ssh_usr": 'lightning',
                "ssh_port": bh['ssh_port'],
                "app_port": bh['app_port'],
                "user_port": bh['user_port'],
                "sparko": 'https://bitclouds.link:' + str(bh['sparko_port'])+'/rpc',
                "ssh2onion": "you can ssh directly to your .onion (/home/lightning/onion.domain) on port 22"
            }

    for bh in p2e_hosts:
        if bh['address'] == host:
            result = {
                "ip": 'pay2exec.dev',
                "ssh_pwd": bh['pwd'],
                "ssh_usr": 'lightning',
                "ssh_port": bh['ssh_port'],
                "app_port": bh['app_port'],
                "web_port": bh['user_port'],
                "sparko": 'https://pay2exec.dev:' + str(bh['sparko_port'])+'/rpc',
                "webapp": 'http://pay2exec.dev:'+str(bh['user_port'])+'/',
                "ssh2onion": "you can open web/ssh directly to your .onion (/home/lightning/onion.domain) on port 80/22"
            }

    for bh in rs_hosts:
        if bh['address'] == host:
            result = {
                "ip": 'bitclouds.link',
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
    desc = 'BitClouds.sh: ' + str(host)
    if sats == 0:
        invoice_data = invoice(amount=0.03, cur='EUR', desc=desc)
        print("generating invoice for 0.03 EUR desc=" + host)
    else:
        print(sats)
        invoice_data = invoice(msat=int(sats)*1000, desc=desc)
        print("generating invoice for " + str(sats) + " sats desc=" + desc)

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
