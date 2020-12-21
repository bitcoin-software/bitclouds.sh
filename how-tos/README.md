#### General commands

List available images:

`$ curl https://bitclouds.sh/images`

```
{
  "images": [
    ...
    "ubuntu",
    ... 
  ]
}
```

*Read more about available images:*

[Ubuntu, Debian, Centos](./linux.md)

[bsdjail](./jail.md)

[bitcoind](./bitcoind.md)

[c-lightning](./bitcoind.md)

[FreeBSD images](./freebsd.md)

*[Market](./market) images:*

[Kubernetes cluster (k8s)](./market/k8s.md)
 
Create instance: 
 
`$ curl https://bitclouds.sh/create/debian`

```
{
  "disclaimer": "If you pay the LN invoice, you agree with terms of service: any abuse usage is prohibited. Your instance may be stopped and/or destroyed at any time without any reason. Do backups. Your data is securely encrypted and instances hosted in enterprise-grade datacenters. Your digital identifiers are logged for authorization purposes. Bitclouds never use your data for any purpose except mentioned above.", 
  "host": "hassaleh", 
  "paytostart": "lnbc990n1p0ak494m560c4gya4t74vptuz39qpp5nhfplt6rzr4wmxd4nprkd3jkssrzd96xxmr0w4j8xxqyjw5qcqpjsp5rw6pu3va62cgajy53qc0dldla93g5rzvxsvzgwxj9xjjysc2sclqrzjqt3xwz3vyes6nm4p8d70mnwh74f0tydeaesw2eut02l80dle29hevzw4suqqgqgqqyqqqqlgqqqqqqgq9q9qy9qsqtg8qrt82t9fy0la0j30rw5g044pt9rfshdcrhzms47jcdp2m6nkkxhvgkfufhtvl3hd3tz7duet5gm46mc2cpmwls47gpvpysrqj5sspa2u99k", 
  "performance": "1xXeon-2GB-40GB", 
  "price": "<1 sat/min", 
  "support": "https://support.bitclouds.sh"
}
```

*After you paid invoice your VPS will be created within a minute*

Check instance status:

`$ curl https://bitclouds.sh/status/hassaleh`

```
{
  "balance": 96, 
  "ip4": "87.85.113.253", 
  "key": "https://bitclouds.sh/key/hassaleh", 
  "status": "subscribed", 
  "tip": "was your recent backup restore succesfull?", 
  "user": "debian"
}
```

Get instance access key:

`$ curl https://bitclouds.sh/key/hassaleh > ssh.key`

Connect to the instance:

`$ ssh -i ssh.key debian@87.85.113.253`

```
------------------: System Data :-------------------------------
Hostname:     hassaleh (10.0.0.13)
Kernel:       4.19.0-13-amd64 (Debian GNU/Linux 10 (buster))
Uptime:       06:55:32 up 9 min,  1 user,  load average: 0.06, 0.03, 0.00
CPU:          Intel(R) Xeon(R) CPU v4 @ 3.60GHz (1 cores)
Memory(Mb):   1 Gb total / 1 Gb free
------------------------: Logged as: [debian]  ------------------------------

For support: https://support.bitclouds.sh


debian@hassaleh:~$ 

```

Add balance to your instance:

`$ curl https://bitclouds.sh/topup/hassaleh` to add 99 sats by default

or `$ curl https://bitclouds.sh/topup/hassaleh/30000` specify amount (*==minutes*) you would like to pay

```
{
  "host": "hassaleh", 
  "invoice": "lnbc300u1p0ak37tpp52et53crpn0ssvh6w9z0v4jy294q7f258gtxw2gz9mres9vuu87lmsjpk423x63sy2s6dxdfkq0vrwcauuwclyzyfqdqadpshxumpd3jkssrzd96xxmr0w4j8xxqyjw5qcqpjsp5tevhmddxe9sc0w2p7s789c4yjmgfdmhtjsu2776cumx7lpgu5hhsrzjqgfursuzjw8vrwhwkut8r0nr62wjt6r8uxmuqu2x3hf2e6jy26z3uzw435qq8zgqqyqqqp9fqqqqqzcqyg9qy9qsq82x88w4ghzheaqgu9nsl3qmcc4hck0um3v2w63tu56j66gyf6zulmmqctvha422kfsptwajcs"
}
```
