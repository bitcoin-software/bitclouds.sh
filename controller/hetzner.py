
from hcloud import Client

from hcloud.images.domain import Image
from hcloud.server_types.domain import ServerType
from hcloud.ssh_keys.client import SSHKeysClient

from ctrldbops import add_hetzner, get_hetzner

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


def createServer(name, image):
    #freebsd = snapid="8322744"
    #image=Image(type="snapshot", id=snapid)
    sysImage = True

    if image=="debian":
        image_name = "debian-10"
    elif image == "centos":
        image_name = "centos-8"
    elif image == "freebsd":
        snap_id = "8322744"
        sysImage = False
    elif image == "ubuntu":
        image_name = "ubuntu"

    if sysImage:
        response = client.servers.create(name=name, server_type=ServerType("cx11"), image=Image(name=image_name))
    else:
        response = client.servers.create(name=name, server_type=ServerType("cx11"), image=Image(type="snapshot", id=snap_id))

    server = response.server

    serverData = dict()

    serverData['id'] = server.id
    serverData['ip'] = server.public_net.ipv4.ip
    serverData['pwd'] = response.root_password

    add_hetzner(name, server.id, server.public_net.ipv4.ip, "cx11", response.root_password)

    return serverData


def deleteServer(id):

    servers = client.servers.get_all()
    for server in servers:
        if server.id == id:
            print(str(id) + " to be deleted")
            server.delete()

    return True
