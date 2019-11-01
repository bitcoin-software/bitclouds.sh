import configparser
import sys


api_config = configparser.ConfigParser()
api_config.read('../controller/config.ini')
project_path = api_config['paths']['local_path']
sys.path.insert(1, project_path + '/controller')
from bitbsd import createbitcoind, createlightningd, delete_jail
from hetzner import createServer, deleteServer, getServers
from ctrldbops import get_bitbsd


def new_server(address, image="debian"):
    if image == "ubuntu" or image == "centos" or image == "debian":
        createServer(address, image)
    elif image=="bitcoind":
        createbitcoind(address)
    elif image=="lightningd":
        createlightningd(address)


def del_server(address):
    bitbsd_servers = get_bitbsd()
    for serv in bitbsd_servers:
        if serv['address'] == address:
            delete_jail(address)

    hetzner_servers =  getServers()

    for serv in hetzner_servers:
        if serv['name'] == address:
            deleteServer(serv['id'])