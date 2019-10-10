
import random
import hmac
from ctrldbops import get_bitbsd, add_bitbsd

from base64 import urlsafe_b64encode
from binascii import hexlify
from os import urandom, system

from passlib.hash import sha512_crypt
import crypt
import getpass;

import configparser

bitbsd_config = configparser.ConfigParser()
bitbsd_config.read('/home/bitclouds/bitclouds/controller/config.ini')


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
    id = 'bd'+generate_salt(4)

    ipv4 = '188.165.223.61'

    ssh_ports = list()
    rpc_ports = list()

    hosts = get_bitbsd()
    for host in hosts:
        ssh_ports.append(host['ssh_port'])
        rpc_ports.append(host['ssh_port'])

    plan = 'bitcoind'

    ssh_port = random.randrange(64002, 64998)
    rpc_port = random.randrange(55002, 55998)
    while ssh_port in ssh_ports:
        ssh_port = random.randrange(64002, 64998)
    while rpc_port in rpc_ports:
        rpc_port = random.randrange(64002, 64998)


    password = generate_password()

    # Create 16 byte hex salt
    salt = generate_salt(16)
    password_hmac = password_to_hmac(salt, password)
    username = id
    authline = 'rpcauth={0}:{1}${2}'.format(username, salt, password_hmac)

    #system("echo '" + authline + "' >> /usr/local/etc/bitcoin.conf")

    rpc_pass = password
    rpc_user = username

    pwd = id
    pwd_sha = crypt.crypt(pwd)
    add_bitbsd(address, id, ipv4, ssh_port, rpc_port, authline, plan, pwd)
    print(pwd)
    system('/usr/local/bin/ansible-playbook /home/bitclouds/bitclouds/controller/playbooks/create_btcnode.yml --extra-vars="cname='+str(id)+' sshport='+str(ssh_port)+' rpcport='+str(rpc_port)+' rpcauthline='+authline+' pwd='+pwd_sha+'"')