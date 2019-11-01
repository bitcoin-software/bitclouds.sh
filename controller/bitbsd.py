
import random
import hmac
from ctrldbops import get_bitbsd, add_bitbsd

from base64 import urlsafe_b64encode
from binascii import hexlify
from os import urandom, system

from passlib.hash import sha512_crypt

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

    hosts = get_bitbsd()
    for host in hosts:
        ssh_ports.append(host['ssh_port'])
        rpc_ports.append(host['ssh_port'])

    plan = 'bitcoind'

    ssh_port = random.randrange(60002, 64998)
    rpc_port = random.randrange(50002, 54998)
    while ssh_port in ssh_ports:
        ssh_port = random.randrange(60002, 64998)
    while rpc_port in rpc_ports:
        rpc_port = random.randrange(50002, 54998)


    password = generate_password()

    # Create 16 byte hex salt
    salt = generate_salt(16)
    password_hmac = password_to_hmac(salt, password)
    username = jail_id
    authline = 'rpcauth={0}:{1}${2}'.format(username, salt, password_hmac)

    #system("echo '" + authline + "' >> /usr/local/etc/bitcoin.conf")

    rpc_pass = password
    rpc_user = username

    #gen user pwd
    pwd = generate_salt(8)

    print(pwd)
    add_bitbsd(address, jail_id, ipv4, ssh_port, rpc_port, authline, rpc_user, rpc_pass, plan, pwd)
    system('/usr/local/bin/ansible-playbook /home/bitclouds/bitclouds/controller/playbooks/create_btcnode.yml --extra-vars="cname='+str(jail_id)+' sshport='+str(ssh_port)+' rpcport='+str(rpc_port)+' rpcauthline='+authline+' rpcusr='+rpc_user+' rpcpwd='+rpc_pass+' pwd='+pwd+'"')


def delete_jail(address):
    jails = get_bitbsd()

    for jail in jails:
        if jail['address'] == address:
            jname = jail['id']
    print('now removing ')
    system(
        '/usr/local/bin/ansible-playbook /home/bitclouds/bitclouds/controller/playbooks/remove_btcnode.yml --extra-vars="jname=' + str(
            jname) + '"')
