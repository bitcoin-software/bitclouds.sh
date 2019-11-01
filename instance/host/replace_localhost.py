import os
import time
import datetime


def get_jails():
    result = list()

    jlist = os.popen("jls | egrep -o '[0-9]+.*192.168.0.[0-9]+'").read()

    lines = jlist.splitlines()

    jails = list()

    for line in lines:
        jid = line.split('  ')[0]
        jip = line.split('  ')[1]
        print(jid + " has " + jip)
        jails.append({"jid": jid, "jip":jip})

    return jails


def replace_hosts(jail):
    os.system('jexec ' + str(jail['jid']) + ' sh -c "cat /etc/hosts | sed \'s/127.0.0.1/' + jail['jip'] + '/g\' > /etc/hosts_new && mv /etc/hosts_new /etc/hosts"')


def check_hosts(jail):
    hasline = os.popen('jexec ' + str(jail['jid']) + ' sh -c "cat /etc/hosts | egrep -o \'127.0.0.1\'"').read()

    return hasline.splitlines()

while True:
    jails = get_jails()

    for jail in jails:
        for line in check_hosts(jail):
            if line == '127.0.0.1':
                replace_hosts(jail)

    time.sleep(30)

