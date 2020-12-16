from flask import Flask, jsonify, request
from wallet import generate_invoice
from stars import getStar
from database import get_hostdata, add_host, register_payment, hide_key
import random
import string


app = Flask(__name__)

app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.url_map.strict_slashes = False

#, 'k8s-beta'
ALL_IMAGES = ['ubuntu', 'bitcoind', 'clightning', 'bsdjail', 'freebsd']


def get_tip():
    tips = [
        '$ cd -',
        '$ cd ~',
        '$ history | grep',
        '$ cmd1 | cmd2_pass_cmd1_output',
        '$ tmux',
        'buy bitcoin!',
        'use *unix!',
        'cloud is just someone else\'s computer'
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
        elif image in ['bitcoind', 'clightning', 'bsdjail']:
            return 'root'

    else:
        return False


@app.route('/create/<image>')
def create_vps(image):

    if image in ALL_IMAGES:
        name = getStar()
        inc = 0

        while get_hostdata(name):
            inc += 1
            name = getStar() + '-' + str(inc)

        #135.125.129.128/26
        add_host(name, get_random_string(12), 'init', image, get_username(image))

        invoice = generate_invoice(99, name)['bolt11']

        result = {
            "host": name,
            "price": "<1 sat/min",
            "perf": "1xXeon-2GB-40GB",
            "paytostart": invoice,
            "disclaimer": "If you pay the LN invoice, you agree with our terms that abuse usage is prohibited."
                          " Your instance may be stopped and destroyed at any time without any reason. Do backups."
                          " Your data is securely encrypted and instances hosted in enterprise-grade datacenters."
                          " Your IP and payment information is logged for authorization purposes."
                          " Bitclouds never use your data for any purpose except mentioned above.",
            "support": "https://support.bitclouds.sh"
        }

        register_payment(name, invoice, "new", get_req_ip())

        return jsonify(result)
    else:
        return {'error': 'no such image'}


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
            "tip": get_tip(),
            "key": "-----BEGIN OPENSSH PRIVATE KEY-----\n"
                   + get_random_string(70) + "\n"
                   + get_random_string(70) + "\n"
                   + get_random_string(70) + "\n"
                   + get_random_string(70) + "\n"
                   + get_random_string(50) + "\n"
                   + "\n-----END OPENSSH PRIVATE KEY-----",
            "status": 'subscribed'
        }

    return result


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
        if hostdata['key_requested'] is False:
            hide_key(host)
            return hostdata['init_priv']
        else:
            return status(host)
    else:
        return False


if __name__ == '__main__':
    app.run(debug=False, port=16444)

