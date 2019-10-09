import configparser
import sys

api_config = configparser.ConfigParser()
api_config.read('../controller/config.ini')
project_path = api_config['paths']['local_path']
sys.path.insert(1, project_path + '/controller')
from hetzner import createServer, deleteServer


def new_server(address, image="freebsd"):
    createServer(address)