from flask import Flask, jsonify, request
from wallet import generate_invoice
from stars import getStar
from database import get_hostdata, add_host, register_payment, hide_key, check_k8s
from nubedb import get_keydata, add_key
import random
import string
import os

app = Flask(__name__)

app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.url_map.strict_slashes = False

#, 'k8s-beta'
MARKET = ['k8s']

ALL_IMAGES = ['ubuntu', 'bitcoind', 'centos', 'clightning',
              'bsdjail', 'lnd', 'freebsd', 'debian', 'freebsd-ufs', 'netbsd', 'openbsd']


def get_tip():
    tips = [
        os.environ['BC_1'],
        os.environ['BC_2'],
        '$ history | grep',
        os.environ['BC_3'],
        '$ tmux',
        'buy bitcoin!',
        'think unix-way!',
        'with great power comes great responsibility',
        'cloud is just someone else\'s computer',
        'was your recent backup restore succesfull?',
        'bhyve intro: https://www.youtube.com/watch?v=aFaLkxwvYZw'
    ]
    return random.choice(tips)


def get_req_ip():
    if request.headers.getlist("X-Forwarded-For"):
        ip = request.headers.getlist("X-Forwarded-For")[0]
    else:
        ip = request.remote_addr

    return ip


def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


def get_username(image):
    if image in ALL_IMAGES:
        if image == 'ubuntu':
            return 'ubuntu'
        if image == 'freebsd':
            return 'freebsd'
        if image == 'netbsd':
            return 'netbsd'
        if image == 'openbsd':
            return 'openbsd'
        if image == 'debian':
            return 'debian'
        if image == 'centos':
            return 'centos'
        if image == 'opnsense':
            return 'opnsense'
        if image == 'lnd':
            return 'lnd'
        elif image in ['bitcoind', 'clightning', 'bsdjail']:
            return 'root'

    else:
        return False


@app.route('/create/<image>')
def create_vps(image):

    setup_fee = 0

    if image in MARKET:
        setup_fee = 9900

        if not check_k8s():
            return jsonify({"error": 'out of stock'})

        name = 'm-' + getStar()
        inc = 0

        while get_hostdata(name):
            inc += 1
            name = 'm-' + getStar() + '-' + str(inc)

        add_host(name, get_random_string(12), 'init', image, get_username(image))

        invoice = generate_invoice(setup_fee+99, name)['bolt11']

        result = {
            "host": name,
            "price": "<1 sat/min",
            "setup_fee": setup_fee,
            "paytostart": invoice,
            "disclaimer":" If you pay the LN invoice, you agree to our terms of service:"
                          " Any usage that can be considered abuse is prohibited."
                          " Your instance may be stopped and/or destroyed at any time without any reason. Do backups."
                          " Your data is securely encrypted and your instances are hosted in enterprise datacenters."
                          " Your digital identifiers are saved for authorization purposes only."
                          " Bitclouds will never use your data for any purpose except mentioned above.",
            "support": "https://support.bitclouds.sh"
        }

        register_payment(name, invoice, "new", get_req_ip())
        return jsonify(result)
    elif image in ALL_IMAGES:
        name = getStar()
        inc = 0

        while get_hostdata(name):
            inc += 1
            name = getStar() + '-' + str(inc)

        add_host(name, get_random_string(12), 'init', image, get_username(image))

        if image == 'lnd':
            setup_fee = 900
        elif image == 'bitcoind':
            setup_fee = 900
        elif image in ['debian', 'ubuntu', 'centos']:
            setup_fee = 0

        invoice = generate_invoice(setup_fee+99, name)['bolt11']

        result = {
            "host": name,
            "price": "<1 sat/min",
            "setup_fee": setup_fee,
            "performance": "1xXeon-2GB-40GB",
            "paytostart": invoice,
            "disclaimer": " If you pay the LN invoice, you agree to our terms of service:"
                          " Any usage that can be considered abuse is prohibited."
                          " Your instance may be stopped and/or destroyed at any time without any reason. Do backups."
                          " Your data is securely encrypted and your instances are hosted in enterprise datacenters."
                          " Your digital identifiers are saved for authorization purposes only."
                          " Bitclouds will never use your data for any purpose except mentioned above.",
            "support": "https://support.bitclouds.sh"
        }

        register_payment(name, invoice, "new", get_req_ip())

        return jsonify(result)
    else:
        return {"error": 'no such image'}


@app.route('/images')
def images():
    result = {
        "images": ALL_IMAGES
    }

    return jsonify(result)


@app.route('/status/<host>')
def status(host):
    hostdata = get_hostdata(host)

    if hostdata:
        if not hostdata['key_requested']:
            key_req = 'https://bitclouds.sh/key/' + host
        else:
            key_req = 'issued'

        if hostdata['status'] == 'subscribed':
            result = {
                "ip4": hostdata['wan_ip'],
                "user": hostdata['username'],
                "key": key_req,
                "tip": get_tip(),
                "status": hostdata['status'],
                "balance": hostdata['balance']
            }
        elif hostdata['status'] == 'inactive':
            result = {
                "ip4": ".".join(map(str, (random.randint(0, 255)
                        for _ in range(4)))),
                "user": hostdata['username'],
                "key": key_req,
                "tip": get_tip(),
                "status": 'inactive'
            }
        elif hostdata['status'] == 'init':
            result = {
                "status": 'unpaid'
            }
    else:
        result = {
            "ip4": ".".join(map(str, (random.randint(0, 255)
                        for _ in range(4)))),
            "user": 'anonymous',
            "tip": get_tip() + str(random.randint(0, 255)),
            "key": "-----BEGIN OPENSSH PRIVATE KEY-----\n"
                   + get_random_string(70) + "\n"
                   + get_random_string(70) + "\n"
                   + get_random_string(70) + "\n"
                   + get_random_string(70) + "\n"
                   + get_random_string(50) + "\n"
                   + "\n-----END OPENSSH PRIVATE KEY-----",
            "status": 'subscribed'
        }

    return jsonify(result)


@app.route('/topup/<host>', defaults={'sats': 99})
@app.route('/topup/<host>/<int:sats>')
def topup(host, sats):

    hostdata = get_hostdata(host)

    if hostdata:
        invoice = generate_invoice(sats, host)['bolt11']
        register_payment(hostdata['name'], invoice, "topup", get_req_ip())

        host_status = hostdata['status']
        if host_status == 'subscribed':
            result = {
                "host": host,
                "invoice": invoice
            }
        else:
            result = {
                "error": "host is expired or not yet initialized"
            }

    else:
        result = {
            "error": "no such host",
        }

    return jsonify(result)


@app.route('/key/<host>')
def getkey(host):
    hostdata = get_hostdata(host)

    if hostdata:
        if hostdata['key_requested'] is False and hostdata['status'] == 'subscribed':
            hide_key(host)
            if hostdata['image'] not in MARKET:
                return hostdata['init_priv']
            else:
                if hostdata['image'] == 'k8s':
                    return hostdata['k8s']['kubeconfig']
        else:
            return status(host)
    else:
        return jsonify(False)


@app.route('/pay/<keyid>', defaults={'sats': 99})
@app.route('/pay/<keyid>/<int:sats>')
def pay(keyid, sats):

    keydata = get_keydata(keyid)

    if keydata:
        invoice = generate_invoice(sats, keyid)['bolt11']
        register_payment(keyid, invoice, "inc", get_req_ip())

        key_status = keydata['status']
        if key_status in ['subscribed', 'new']:
            result = {
                "cid": keyid,
                "invoice": invoice
            }
        else:
            result = {
                "error": "error message - key status new or not subscribed"
            }
    else:
        result = {
            "error": "no such key",
            "action": "key record created"
        }

    return jsonify(result)


@app.route('/balance/<keyid>')
def balance(keyid):
    keydata = get_keydata(keyid)

    return keydata


if __name__ == '__main__':
    app.run(debug=False, port=16444)



