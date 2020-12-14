from flask import Flask, jsonify
from wallet import generate_invoice
from stars import getStar
from database import get_hostdata, add_host
import random
import string


app = Flask(__name__)

app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.url_map.strict_slashes = False

#, 'k8s-beta'
ALL_IMAGES = ['ubuntu-eu', 'bitcoind', 'bsdjail']


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

        result = {
            "name": name
        }

        #135.125.129.128/26
        add_host(name, '0.0.0.0', get_random_string(12), 'init', image)

        result = {
            "host": name,
            "paytostart": generate_invoice(99, name)['bolt11']
        }

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

    if hostdata:
        status = hostdata['status']
        if status == 'subscribed':
            result = {
                "host": host,
                "invoice": generate_invoice(sats, host)['bolt11']
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


if __name__ == '__main__':
    app.run(debug=False, port=16444)
