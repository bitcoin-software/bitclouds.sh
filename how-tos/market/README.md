#### Market images

Bitclouds offers images from market. These are special images sold by community members.

Market images may have limited stock:

`$ curl https://bitclouds.sh/create/k8s`

```
{
"error": "out of stock"
}
```

One-time setup fee of 9900 satoshi is applied for market instances

`$ curl https://bitclouds.sh/create/k8s`

```
{
...
  "price": "<1 sat/min", 
  "setup_fee": "9900 sats",
 ... 
}
```

Usually, market instance name has `m-` prefix (i.e. `m-alpherg`) in it's name

Currently available only [k8s](./k8s.md) image in market