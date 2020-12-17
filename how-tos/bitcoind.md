#### Bitcoind (Bitcoin Core node)

You can order a fully synced `bitcoind` node

Bitcoin Core in FreeBSD jail with `root` access and completely dedicated datadir

After first login, consider to replace default issued ssh access key and set password for user *freebsd* and/or root if required.

SSH password authentication is disabled by default

Inside instance you can execute `bitcoin-cli` commands

`aladfar:/root@[13:08] # bitcoin-cli getblockchaininfo`

```
{
  "chain": "main",
  "blocks": 661744,
  "headers": 661744,
  "bestblockhash": "000000000000000000020f29eb5c90e6e48ce687b546d3fb499ab6d977af1c07",
  "difficulty": 18670168558399.59,
  "mediantime": 1608206293,
  "verificationprogress": 0.9999949501179342,
  "initialblockdownload": false,
  "chainwork": "000000000000000000000000000000000000000016f90c9acb758a775a014c77",
  "size_on_disk": 359058733092,
  "pruned": false,
  "softforks": {
    "bip34": {
      "type": "buried",
      "active": true,
      "height": 227931
    },
    "bip66": {
      "type": "buried",
      "active": true,
      "height": 363725
    },
    "bip65": {
      "type": "buried",
      "active": true,
      "height": 388381
    },
    "csv": {
      "type": "buried",
      "active": true,
      "height": 419328
    },
    "segwit": {
      "type": "buried",
      "active": true,
      "height": 481824
    }
  },
  "warnings": ""
}

```

And edit the configuration of `bitcoind` in `

`aladfar:/root@[13:08] # ls -la /usr/local/etc/`

```
...
-rw-r--r--   1 root  wheel  1232 Dec 17 13:06 bitcoin.conf
-rw-r--r--   1 root  wheel   704 Oct  4 21:15 bitcoin.conf.sample
...
```

To apply configuration, stop and start `bitcoind`

```
aladfar:/root@[13:09] # bitcoin-cli stop
Bitcoin Core stopping
```

```
aladfar:/root@[13:10] # service bitcoind start
Performing sanity check on bitcoind configuration:
Bitcoind is not running
Starting bitcoind:
```

Check status:

```
aladfar:/root@[13:11] # ps -aux | grep bitcoin
bitcoin 32845 172.3  1.3 2529252 855236  -  SNsJ 13:11   0:15.17 
/usr/local/bin/bitcoind -conf=/usr/local/etc/bitcoin.conf -datadir=/var/db/bitcoin
```

Access `bitcoind` datadir

`aladfar:/root@[13:11] # ls -la /var/db/bitcoin/`

```
-rw-------   1 bitcoin  bitcoin         0 Nov  3 17:14 .lock
-rw-------   1 bitcoin  bitcoin         0 Nov  3 17:15 .walletlock
-rw-------   1 bitcoin  bitcoin        37 Nov  3 17:15 banlist.dat
-rw-------   1 bitcoin  bitcoin         6 Dec 17 13:11 bitcoind.pid
drwx------   3 bitcoin  bitcoin      4735 Dec 17 08:10 blocks
drwx------   2 bitcoin  bitcoin      2142 Dec 17 13:11 chainstate
drwx------   2 bitcoin  bitcoin         3 Dec 17 13:11 database
-rw-------   1 bitcoin  bitcoin         0 Nov  3 17:15 db.log
-rw-------   1 bitcoin  bitcoin  10312426 Dec 17 13:12 debug.log
-rw-------   1 bitcoin  bitcoin    247985 Dec 17 13:10 fee_estimates.dat
-rw-------   1 bitcoin  bitcoin  32179889 Dec 17 13:10 mempool.dat
-rw-------   1 bitcoin  bitcoin   4140208 Dec 17 13:10 peers.dat
-rw-------   1 bitcoin  bitcoin   1490944 Dec 17 13:11 wallet.dat
```