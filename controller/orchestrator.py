from bitbsd import createbitcoind, createlightningd, createrootshell, delete_jail, createp2e
from hetzner import createServer, deleteServer, getServers
from ctrldbops import get_bitbsd, find_hosts


def new_server(address, image="debian"):
    if image == "ubuntu" or image == "centos" or image == "debian" or image == "vpn":
        createServer(address, image)
    elif image=="bitcoind":
        createbitcoind(address)
    elif image=="lightningd":
        createlightningd(address)
    elif image=="rootshell":
        createrootshell(address)
    elif image=="pay2exec":
        createp2e(address)


def del_server(address):
    hosts = find_hosts()
    for host in hosts:
        if address == host['address']:
            image = host['image']

    bitbsd_servers = get_bitbsd(image)
    for serv in bitbsd_servers:
        if serv['address'] == address:
            delete_jail(address)

    hetzner_servers =  getServers()

    for serv in hetzner_servers:
        if serv['name'] == address:
            deleteServer(serv['id'])
