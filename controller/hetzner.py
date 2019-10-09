
from hcloud import Client

from hcloud.images.domain import Image
from hcloud.server_types.domain import ServerType
from hcloud.ssh_keys.client import SSHKeysClient


import configparser

hetzner_config = configparser.ConfigParser()
hetzner_config.read('/home/bitclouds/bitclouds/controller/config.ini')

hetzner_token = hetzner_config['hetzner']['api_key']

client = Client(token=hetzner_token)  # Please paste your API token here between the quotes
sshClient = SSHKeysClient(client)


def getServers():
    hetzner_servers = client.servers.get_all()

    servers = list()

    for server in hetzner_servers:
        serverData = dict()

        serverData['id'] = server.id
        serverData['ip'] = server.public_net.ipv4.ip
        serverData['name'] = server.name

        servers.append(serverData)

    return servers


def createServer(name, snapid="8322744"):
    mykeys = list()
    for key in sshClient.get_all():
        mykeys.append(key)

    response = client.servers.create(name=name, server_type=ServerType("cx11"), image=Image(type="snapshot", id=snapid), ssh_keys=mykeys)
    server = response.server

    serverData = dict()

    serverData['id'] = server.id
    serverData['ip'] = server.public_net.ipv4.ip

    return serverData


def deleteServer(id):

    servers = client.servers.get_all()
    for server in servers:
        if server.id == id:
            print(str(id) + " to be deleted")
            server.delete()

    return True