from flask import Flask, jsonify
from wallet import generate_invoice
from stars import getStar
from database import find_host

app = Flask(__name__)

app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.url_map.strict_slashes = False


@app.route('/create/<image>')
def create_vps(image):

    all_images = ['ubuntu-eu']

    if image in all_images:
        name = getStar()
        inc = 0
        while find_host(name):
            inc += 1
            name = getStar() + '-' + str(inc)

        result = {
            "name": name
        }

        result = {
            "host": name,
            "paytostart": generate_invoice(99,name)['bolt11']
        }

        return jsonify(result)
    else:
        return {'error': 'no such image'}


@app.route('/images')
def images():
    result = {
        "images": ['ubuntu-eu']
    }

    return jsonify(result)


@app.route('/status/<host>')
def status(host):
    result = {
        "status": "we are still on the way"
    }

    return result


@app.route('/topup/<host>', defaults={'sats': 1})
@app.route('/topup/<host>/<int:sats>')
def topup(host, sats):

    result = {
        "topup-"+host: sats
    }

    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=False, port=16444)
