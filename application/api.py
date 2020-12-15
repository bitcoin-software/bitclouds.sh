from flask import Flask, jsonify, request
from wallet import generate_invoice
from stars import getStar
from database import get_hostdata, add_host, register_payment
import random
import string


app = Flask(__name__)

app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.url_map.strict_slashes = False

#, 'k8s-beta'
ALL_IMAGES = ['ubuntu-eu', 'bitcoind', 'bsdjail']


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


@app.route('/create/<image>')
def create_vps(image):

    if image in ALL_IMAGES:
        name = getStar()
        inc = 0

        while get_hostdata(name):
            inc += 1
            name = getStar() + '-' + str(inc)

        #135.125.129.128/26
        add_host(name, '0.0.0.0', get_random_string(12), 'init', image)

        invoice = generate_invoice(99, name)['bolt11']

        result = {
            "host": name,
            "paytostart": invoice
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
    result = {
        "status": "we are still on the way"
    }

    return result


@app.route('/topup/<host>', defaults={'sats': 99})
@app.route('/topup/<host>/<int:sats>')
def topup(host, sats):

    hostdata = get_hostdata(host)

    invoice = generate_invoice(sats, host)['bolt11']

    if hostdata:
        register_payment(hostdata['name'], invoice, "topup", get_req_ip())

        host_status = hostdata['status']
        if host_status == 'subscribed':
            result = {
                "host": host,
                "invoice": invoice
            }
            register_payment()
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

    return hostdata['init_priv']


if __name__ == '__main__':
    app.run(debug=False, port=16444)

