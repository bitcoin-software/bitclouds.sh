from flask import Flask, request, jsonify
import datetime
from btc_wallet import bstartd, bgetunused, bgetnew, bnotify, bstopd, blistunspent
from stars import getStar
from dbops import find_host, create_host, subscribe_host, add_tx, find_tx, update_tx
from tgcontrol import ticket_notify
import sys
import time
import random, string
import re
import os

from common import config
from common.charge import get_invoice

wallet = config["electrum"]["wallet"]

app = Flask(__name__)

project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
controller_path = os.path.join(project_path, "controller")
sys.path.insert(1, controller_path)

task_running = False

from orchestrator import new_server


def convert_sats2hours(address, sats):
        hours = int(sats / 66)
        if hours < 0:
            hours = 0

        return hours


@app.route('/elify', methods=['POST'])
def elify():
    dtime = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
    data = request.get_json()
    status = '['+data['status']+']'
    address = '['+data['address']+']'

    print(dtime + " new status " + status + " for " + address)
    if status != '':
        unspents = blistunspent(wallet)
        #print(unspents)
        for unspent in unspents:
            if address == unspent['address']:
                amount_sats = unspent['value']*100000000
                outhash = status
                prev_outhash = unspent['prevout_hash']
                if unspent['height'] == 0:
                    if not find_tx(outhash):
                        add_tx(address=address, txhash=outhash, amount_sats=amount_sats, status='paid', chargeid='none', prev_outhash=prev_outhash)
                    else:
                        print(dtime + 'tx already exists')
                elif unspent['height'] > 0:
                    existing_tx = find_tx(outhash)
                    if existing_tx:
                        if existing_tx['status'] == 'paid':

                            new_host = find_host(address)
                            if new_host:
                                if new_host['status'] == 'new':
                                    global task_running
                                    while task_running:
                                        time.sleep(30)
                                    task_running = True
                                    if task_running:
                                        _ = new_server(address, new_host['image'])
                                    task_running = False

                            update_tx(address, outhash, 'confirmed')
                            hours = convert_sats2hours(address, amount_sats)
                            subscribe_host(address, hours)
                            print("\n\n" + str(find_host(address)) + "\n\n")
                        else:
                            print(dtime + ' ' + outhash + 'tx already confirmed')
                    else:
                        print(dtime + ' ' + outhash + ' tx not found but confirmed')

    return ''


@app.route('/chargify', methods=['POST'])
def chargify():
    dtime = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
    id = request.get_json()['id']
    invoice_data = get_invoice(id=id)
    #print(invoice_data)
    address = str(invoice_data['description']).replace('BitClouds.sh: ', '')
    status = invoice_data['status']
    amount_sats = int(int(invoice_data['msatoshi'])/1000)
    bolt = invoice_data['payreq']
    print(dtime + " new status [" + status + "] for [" + id + "]")
    if status == 'paid':
        new_host = find_host(address)
        if new_host:
            if new_host['status'] == 'new':
                global task_running
                while task_running:
                    time.sleep(30)
                task_running = True
                if task_running:
                    _ = new_server(address, new_host['image'])
                    time.sleep(15)
                task_running = False
        add_tx(address=address, txhash=bolt, amount_sats=amount_sats, status='confirmed', chargeid=id, prev_outhash='none')
        hours = convert_sats2hours(address, amount_sats)
        subscribe_host(address, hours)
    print("\n" + dtime + " TOP-UP " + str(find_host(address)) + "\n\n")
    return ''


@app.route('/support', methods=['POST'])
def support():
    dtime = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
    id = request.get_json()['id']
    invoice_data = get_invoice(id=id)
    desc = invoice_data['description']
    status = invoice_data['status']
    amount_sats = int(int(invoice_data['msatoshi'])/1000)
    bolt = invoice_data['payreq']
    # *[support BitClouds.sh] | malto-1 | tet@tet.com:~ help
    m = re.search('^(.*)\[support BitClouds\.sh\] \| ([a-z\-0-9]+) \| (.*):~ (.*)', desc)

    premium = m.group(1)
    address = m.group(2)
    contact = str(m.group(3))
    msg = str(m.group(4))

    print(dtime + " " + status + " support message [" + address + "] for [" + contact + "]")
    if status == 'paid':
        ticket_notify(premium, address, contact, msg)
    return ''



def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))


@app.route('/newaddr', methods=['POST'])
def newaddr():
    dtime = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')

    #address = str(bgetunused(wallet).rstrip())

    image = request.form['image']

    address = getStar()
    inc = 0
    while find_host(address):
        inc+=1
        address = getStar()+'-'+str(inc)

    result = {
        "address": address
    }

    print(dtime)
    print("new addr:" + address + ";\nwill notify:" + notifyURL + ";\n")
    #bnotify(wallet, address, notifyURL)
    create_host(address, "basic", image)

    return jsonify(result)


if __name__ == "__main__":
    #    wallet_list = [wallet]
    #    bstopd()
    #    bstartd(wallet_list)

    notifyURL = config['ipn']['url'] + '/elify'
    #    addr = bgetunused(wallet)

    app.run(debug=config['environment']['debug'] == 'true', host=config['wallet']['ip'], port=config['wallet']['port'])
