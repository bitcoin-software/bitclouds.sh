### BitClouds.sh - open-source programmable VPS platform ###

### Bitclouds is temporary down, we are moving to new backend and re-factoring the code

Bitclouds is a streaming cloud platform. You can order instances on per-minute accounting. You can create new instance right from your app or script, or simply manually with `curl`:

`$ curl https://bitclouds.sh/images`

_{
  "images": [
    "ubuntu", 
  ]
}_
 
`$ curl https://bitclouds.sh/create/ubuntu`

_{
  "host": "Alya", 
  "paytostart": "lnbc3637390p1pwmepx3pp54n6zwvchgay8sxxzu7323puzqtwc8wqxtjhmngl4f2myvyv90w6sdq8g9k8jcgxqzjccqp2rzjqgzgmxw0f8zd5slh03p5nrmqnkyjlyyxwh8gduecvp5el0ujw7jcxzg6jyqqfdsqqqqqqqlgqqqqqqgq9q4fjezksy4z8tcg3hyfexkqguzcnjhczdqgpp5mzwjqk7fgjf2cspvvns0r29dnzrvh3846rey58d7vjyqrsc5a70mjl4fg2zwamzp6cptva0k2"
}_

After you paid invoice your VPS will be created within a minute or two

### Setting up your own bitclouds:

0) [FreeBSD](https://www.freebsd.org/) host with [cbsd](https://github.com/olevole/cbsd)

1) `tcsh misc/setenvs.sh`

2) `pip install -r application/requirements.txt`

