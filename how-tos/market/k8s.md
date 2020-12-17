#### Kubernetes cluster

Create image:

`$ curl https://bitclouds.sh/create/k8s`

```
{
  "disclaimer": "If you pay the LN invoice, you agree with terms of service: any abuse usage is prohibited. Your instance may be stopped and/or destroyed at any time without any reason. Do backups. Your data is securely encrypted and instances hosted in enterprise-grade datacenters. Your IP and payment information is logged for authorization purposes. Bitclouds never use your data for any purpose except mentioned above.", 
  "host": "m-alpherg", 
  "paytostart": "lnbc99990n1p0akcm6pp5lwrq8a4nztensdqld5kkzmrsdpjhye6qvf5hy2vxpqajwp9v7pdx2zcndl5t2shwpge5gn3kfs0a8mv9vgsld6uxrwp8g29m7n5lufqjhcg70lc503y0zp2qqrzjqgqyccjavg3y2cr2r63vr35uldz3ddcrk3u5tgmywufuqhly4t43czw43cqqw6cqqyqqqqlgqqqqqqgq9q9qy9qsqjpzpkp73hjvyd34z9ugx9tggcx2eztrlwfsdk0x2r2wqv39y7779zmt6ahs7ukt2kvddh845ac69pkf0m383x5njwexusu7q9s8lrxgqqk6y3h", 
  "price": "<1 sat/min", 
  "setup_fee": "9900 sats", 
  "support": "https://support.bitclouds.sh"
}
```

Copy kubeconfig to your `~/.kube/config`:

`$ curl https://bitclouds.sh/key/m-alpherg > ~/.kube/config`

Check cluster status:

`$ kubectl get nodes`

```
NAME      STATUS   ROLES    AGE    VERSION
master1   Ready    master   156m   v1.19.4`
```

Deploy sample YML:

`user@local:/home/user/k8s_deployments$ kubectl apply -f sample_deploy.yml`