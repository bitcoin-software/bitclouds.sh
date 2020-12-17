#### Bitcoind (Bitcoin Core node)

You can order a fully operational `c-lightning` node

[c-lightning](https://github.com/ElementsProject/lightning) in FreeBSD jail with `root` access and completely dedicated datadir (but shared bitcoind)

After first login, consider to replace default issued ssh access key and set password for user *freebsd* and/or root if required.

SSH password authentication is disabled by default

Inside instance you can execute `lightning-cli` commands

Before you start, you may want to install text editor with `pkg install -y nano`

`muphrid:/root@[13:28] # lightning-cli getinfo`

```
{
   "id": "02a6db7b91ba805687eb668d3d776b1ef5c4b90118992feb172e6a7b297179410d",
   "alias": "clightning@bitclouds.sh",
   "color": "02a6db",
   "num_peers": 0,
   "num_pending_channels": 0,
   "num_active_channels": 0,
   "num_inactive_channels": 0,
   "address": [
      {
         "type": "ipv4",
         "address": "85.241.9.25",
         "port": 9735
      }
   ],
   "binding": [],
   "version": "0.8.2.1",
   "blockheight": 661746,
   "network": "bitcoin",
   "msatoshi_fees_collected": 0,
   "fees_collected_msat": "0msat",
   "lightning-dir": "/var/db/c-lightning/bitcoin"
}
```

Edit the with text editor (i.e. `nano`) your configuration of `lightningd` in 

`muphrid:/root@[13:28] # ls -la /usr/local/etc/`
```
...
-r--------   1 c-lightning  c-lightning  2155 Dec 17 13:27 lightningd-bitcoin.conf
-r--------   1 c-lightning  c-lightning   730 Dec 12 05:25 lightningd-bitcoin.conf.sample
...
```

To apply configuration, stop and start `lightningd`

```
muphrid:/root@[13:29] # lightning-cli stop
"Shutdown complete"
```

```
muphrid:/root@[13:33] # service lightningd start
Waiting for bitcoind to start serving RPC, lightningd cannot start without it 20
...
Waiting for bitcoind to start serving RPC, lightningd cannot start without it 1
eval: bitcoin-cli: not found
Failed: bitcoind did not start serving RPC, starting lightningd anyway
Starting lightningd.
plugin-sparko  initialized plugin v2.5
plugin-sparko  Login credentials read: qzuoulyjtm:rghpxycumm (full-access key: cUNipCvymI5SVgC9u0C1rGYOS0qb9S22xBUMaMwuM)
plugin-sparko 2 keys read: skdoukezwd (full-access), pzkebdmluz (3 permission)
plugin-sparko  HTTP server on http://0.0.0.0:9737/
```

Your `c-lightning` node is powered with [Sparko plugin](https://github.com/fiatjaf/sparko), 
so you have HTTP API for `c-lighning` out of the box.
Simply `curl` you public IP from your local terminal:

`you@laptop # curl -k https://85.241.9.25/rpc -d '{"method": "getinfo"}' -H 'X-Access: cUNipCvymI5SVgC9u0C1rGYOS0qb9S22xBUMaMwuM'`

```
{
    "id":"02a6db7b91ba805687eb668d3d776b1ef5c4b90118992feb172e6a7b297179410d",
    "alias":"clightning@bitclouds.sh",
    "color":"02a6db",
    "num_peers":0,
    "num_pending_channels":0,
    "num_active_channels":0,
    "num_inactive_channels":0,
    "address":[
    {
        "type":"ipv4",
        "address":"85.241.9.25",
        "port":9735}
    ],
    "binding":[],
    "version":"0.8.2.1",
    "blockheight":661746,
    "network":"bitcoin",
    "msatoshi_fees_collected":0,
    "fees_collected_msat":"0msat",
    "lightning-dir":"/var/db/c-lightning/bitcoin"
}
```

You may want to use your own dedicated bitcoin RPC, to do so, order a bitclouds `bitcoind`
or point your `lightnind` to existing `bitcoind` node:

`muphrid:/root@[13:47] # nano /usr/local/etc/lightningd-bitcoin.conf`

```
...
bitcoin-rpcconnect=10.15.0.1
bitcoin-rpcpassword=Hszd_4vr53634345vvsdFLLNnfw422f5a2f6=
bitcoin-rpcport=8332
bitcoin-rpcuser=845Fd332
...

```

