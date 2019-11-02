
import random
import hmac
from ctrldbops import get_bitbsd, add_bitbsd, add_bitbsd_cln, add_bitbsd_rs, find_hosts

from base64 import urlsafe_b64encode
from binascii import hexlify
from os import urandom, system

from get_lnrpc import getrpc

import configparser

bitbsd_config = configparser.ConfigParser()
bitbsd_config.read('/home/bitclouds/bitclouds/controller/config.ini')

host_ip = bitbsd_config['bitbsd']['host_ip']


def generate_salt(size):
    """Create size byte hex salt"""
    return hexlify(urandom(size)).decode()


def generate_password():
    """Create 32 byte b64 password"""
    return urlsafe_b64encode(urandom(32)).decode('utf-8')


def password_to_hmac(salt, password):
    m = hmac.new(bytearray(salt, 'utf-8'), bytearray(password, 'utf-8'), 'SHA256')
    return m.hexdigest()


def createbitcoind(address):
    jail_id = 'bd'+generate_salt(4)

    ipv4 = host_ip

    ssh_ports = list()
    rpc_ports = list()

    hosts = get_bitbsd('bitcoind')
    for host in hosts:
        ssh_ports.append(host['ssh_port'])
        rpc_ports.append(host['rpc_port'])

    plan = 'bitcoind'

    ssh_port = random.randrange(60002, 61000)
    rpc_port = random.randrange(50002, 51000)
    while ssh_port in ssh_ports:
        ssh_port = random.randrange(60002, 61000)
    while rpc_port in rpc_ports:
        rpc_port = random.randrange(50002, 51000)

    rpc_password = generate_password()

    # Create 16 byte hex salt
    salt = generate_salt(16)
    password_hmac = password_to_hmac(salt, rpc_password)
    username = jail_id
    authline = 'rpcauth={0}:{1}${2}'.format(username, salt, password_hmac)

    #system("echo '" + authline + "' >> /usr/local/etc/bitcoin.conf")

    rpc_pass = rpc_password
    rpc_user = username

    #gen user pwd
    pwd = generate_salt(8)

    print(pwd)
    add_bitbsd(address, jail_id, ipv4, ssh_port, rpc_port, authline, rpc_user, rpc_pass, plan, pwd)
    system('/usr/local/bin/ansible-playbook /home/bitclouds/bitclouds/controller/playbooks/create_btcnode.yml --extra-vars="cname='+str(jail_id)+' sshport='+str(ssh_port)+' rpcport='+str(rpc_port)+' rpcauthline='+authline+' rpcusr='+rpc_user+' rpcpwd='+rpc_pass+' pwd='+pwd+'"')


def createlightningd(address):
    jail_id = 'cln'+generate_salt(4)

    ipv4 = host_ip

    ssh_ports = list()
    app_ports = list()
    sparko_ports = list()
    user_ports = list()

    hosts = get_bitbsd('lightningd')
    for host in hosts:
        try:
            ssh_ports.append(host['ssh_port'])
            app_ports.append(host['app_port'])
            sparko_ports.append(host['sparko_port'])
            user_ports.append(host['user_port'])
        except KeyError as e:
            print('ignoring ' + host['address'])

    plan = 'lightningd'

    ssh_port = random.randrange(61002, 62000)
    sparko_port = random.randrange(59002, 59999)
    app_port = random.randrange(51002, 52000)
    user_port = random.randrange(53002, 54000)
    while ssh_port in ssh_ports:
        ssh_port = random.randrange(61002, 62000)
    while app_port in app_ports:
        app_port = random.randrange(51002, 52000)
    while sparko_port in sparko_ports:
        sparko_port = random.randrange(59002, 59999)
    while user_port in user_ports:
        user_port = random.randrange(53002, 54000)

    sparko1 = 'M'+generate_salt(8)
    sparko2 = 'R'+generate_salt(8)
    sparko3 = 'RW'+generate_salt(8)

    creds = getrpc()

    rpc_user = creds['user']
    rpc_pass = creds['password']

    authline = 'None'

    alias = address + " [bitclouds.sh]"

    #gen user pwd
    pwd = generate_salt(8)

    ports = {
        'ssh': ssh_port,
        'app': app_port,
        'sparko': sparko_port,
        'userport': user_port
    }

    print(pwd)
    add_bitbsd_cln(address, jail_id, ipv4, ports, alias, rpc_user, rpc_pass, plan, pwd)
    system('/usr/local/bin/ansible-playbook /home/bitclouds/bitclouds/controller/playbooks/create_lightningd.yml --extra-vars="cname='+str(jail_id)+' sshport='+str(ssh_port)+' appport='+str(app_port)+' sparko1='+str(sparko1)+' sparko2='+str(sparko2)+' sparko3='+str(sparko3)+' sparkoport='+str(sparko_port)+' userport='+str(user_port)+' alias='+alias+' rpcusr='+rpc_user+' rpcpwd='+rpc_pass+' pwd='+pwd+'"')


def createrootshell(address):
    jail_id = 'rs'+generate_salt(4)

    ipv4 = host_ip

    ssh_ports = list()
    app_ports = list()

    hosts = get_bitbsd('rootshell')
    for host in hosts:
        ssh_ports.append(host['ssh_port'])
        app_ports.append(host['app_port'])

    plan = 'rootshell'

    ssh_port = random.randrange(62002, 63000)
    app_port = random.randrange(52002, 53000)
    while ssh_port in ssh_ports:
        ssh_port = random.randrange(62002, 63000)
    while app_port in app_ports:
        app_port = random.randrange(52002, 53000)

    creds = getrpc()

    rpc_user = creds['user']
    rpc_pass = creds['password']

    authline = 'None'

    alias = address + " [bitclouds.sh]"

    #gen user pwd
    pwd = generate_salt(8)

    print(pwd)
    add_bitbsd_rs(address, jail_id, ipv4, ssh_port, app_port, plan, pwd)
    system('/usr/local/bin/ansible-playbook /home/bitclouds/bitclouds/controller/playbooks/create_rootshell.yml --extra-vars="cname='+str(jail_id)+' sshport='+str(ssh_port)+' pwd='+pwd+'"')


def delete_jail(address):
    hosts = find_hosts()
    for host in hosts:
        if address == host['address']:
            image = host['image']

    jails = get_bitbsd(image)

    for jail in jails:
        if jail['address'] == address:
            starname = jail['address']
            jname = jail['id']

    print('now removing from bitbsd ' + starname + "(" + jname + ")")
    system(
        '/usr/local/bin/ansible-playbook /home/bitclouds/bitclouds/controller/playbooks/remove_btcnode.yml --extra-vars="jname=' + str(
            jname) + '"')
