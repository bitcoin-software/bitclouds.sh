#!/usr/bin/env python3
# Copyright (c) 2015-2018 The Bitcoin Core developers
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.

from argparse import ArgumentParser
from base64 import urlsafe_b64encode
from binascii import hexlify
from getpass import getpass
from os import urandom, system

import hmac


def generate_salt(size):
    """Create size byte hex salt"""
    return hexlify(urandom(size)).decode()


def generate_password():
    """Create 32 byte b64 password"""
    return urlsafe_b64encode(urandom(32)).decode('utf-8')


def password_to_hmac(salt, password):
    m = hmac.new(bytearray(salt, 'utf-8'), bytearray(password, 'utf-8'), 'SHA256')
    return m.hexdigest()


def main():

    password = generate_password()

    # Create 16 byte hex salt
    salt = generate_salt(16)
    password_hmac = password_to_hmac(salt, password)
    username = generate_salt(4)
    authline = 'rpcauth={0}:{1}${2}'.format(username, salt, password_hmac)

    system("echo '" + authline + "' >> /usr/local/etc/bitcoin.conf")
    print("your rpc user:" + username)
    print("your rpc pwd:" + username)


if __name__ == '__main__':
    main()
