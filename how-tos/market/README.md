#### Market images

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
