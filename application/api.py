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
    if image in ['eu-ubuntu']:

        result = {
            "host": "barnardstar-420",
            "paytostart": "bolt"
        }

        return jsonify(result)
    else:
        return {'error': 'no such image'}


@app.route('/images')
def images():
    result = {
        "images": ['eu-ubuntu'] #'freebsd', 'bitcoind', 'lightningd'
    }

    return jsonify(result)


@app.route('/status/<host>')
def status(host):
    result = {
        "status": "none"
    }

    return result


@app.route('/topup/<host>', defaults={'sats': 1})
@app.route('/topup/<host>/<int:sats>')
def topup(host, sats):

    result = {
        "topup-"+host: sats #'freebsd', 'bitcoind', 'lightningd'
    }

    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=False, port=16444)
