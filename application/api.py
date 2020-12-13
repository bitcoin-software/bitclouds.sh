from flask import Flask, jsonify
from wallet import generate_invoice
from stars import getStar
from database import find_host, add_host

app = Flask(__name__)

app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.url_map.strict_slashes = False

ALL_IMAGES = ['ubuntu-eu', 'k8s-beta', 'bsdjail']


@app.route('/create/<image>')
def create_vps(image):

    if image in ALL_IMAGES:
        name = getStar()
        inc = 0

        while find_host(name):
            inc += 1
            name = getStar() + '-' + str(inc)

        result = {
            "name": name
        }

        add_host(name, '135.125.129.128/26', 'password', 'init')

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

    result = {
        "host": host,
        "invoice": generate_invoice(sats, host)['bolt11']
    }

    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=False, port=16444)
