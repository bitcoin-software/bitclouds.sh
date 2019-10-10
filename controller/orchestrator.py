import configparser
import sys


api_config = configparser.ConfigParser()
api_config.read('../controller/config.ini')
project_path = api_config['paths']['local_path']
sys.path.insert(1, project_path + '/controller')
from bitbsd import createbitcoind
from hetzner import createServer, deleteServer
from ctrldbops import get_bitbsd


def new_server(address, image="debian"):
    if image == "ubuntu" or image == "centos" or image == "debian":
        createServer(address, image)
    elif image=="bitcoind":
        createbitcoind(address)


def del_server(address):
    servers = get_bitbsd()
    for serv in servers:
        if serv['address'] == address:
            pass