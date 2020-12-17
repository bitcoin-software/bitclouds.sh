#### FreeBSD jails

Lightweight FreeBSD containers (jails) are available with image ***bsdjail***

All images are preconfigured with latest release base

After first login, consider to replace default issued ssh access key and set password for root if required.

SSH password authentication is disabled by default

You can search for packages:

```
tiaki:/root@[12:44] # pkg search nginx

modsecurity3-nginx-1.0.1_1     Instruction detection and prevention engine / nginx Wrapper
nginx-1.18.0_25,2              Robust and small WWW server
nginx-devel-1.19.3_3           Robust and small WWW server
nginx-full-1.18.0_5,2          Robust and small WWW server (full package)
nginx-lite-1.18.0_25,2         Robust and small WWW server (lite package)
nginx-naxsi-1.18.0_25,2        Robust and small WWW server (plus NAXSI)
nginx-prometheus-exporter-0.8.0 Prometheus exporter for NGINX and NGINX Plus stats
nginx-ultimate-bad-bot-blocker-4.2020.03.2005_1 Nginx bad bot and other things blocker
nginx-vts-exporter-0.10.3      Server that scraps NGINX vts stats and export them via HTTP
p5-Nginx-ReadBody-0.07_1       Nginx embeded perl module to read and evaluate a request body
p5-Nginx-Simple-0.07_1         Perl 5 module for easy to use interface for Nginx Perl Module
p5-Test-Nginx-0.28             Testing modules for Nginx C module development
py27-certbot-nginx-1.8.0       NGINX plugin for Certbot
py37-certbot-nginx-1.8.0       NGINX plugin for Certbot
rubygem-passenger-nginx-6.0.6  Modules for running Ruby on Rails and Rack applications

```

And install packages:

```
tiaki:/root@[12:44] # pkg install -y bash
Updating FreeBSD repository catalogue...
FreeBSD repository is up to date.
All repositories are up to date.
Updating database digests format: 100%
The following 4 package(s) will be affected (of 0 checked):

New packages to be INSTALLED:
	bash: 5.0.18_3
	gettext-runtime: 0.21
	indexinfo: 0.3.1
	readline: 8.0.4

Number of packages to be installed: 4

The process will require 11 MiB more space.
2 MiB to be downloaded.
[tiaki.bitclouds.sh] [1/4] Fetching bash-5.0.18_3.txz: 100%    1 MiB   1.5MB/s    00:01    
[tiaki.bitclouds.sh] [2/4] Fetching indexinfo-0.3.1.txz: 100%    6 KiB   5.8kB/s    00:01    
[tiaki.bitclouds.sh] [3/4] Fetching readline-8.0.4.txz: 100%  354 KiB 362.2kB/s    00:01    
[tiaki.bitclouds.sh] [4/4] Fetching gettext-runtime-0.21.txz: 100%  165 KiB 168.9kB/s    00:01    
Checking integrity... done (0 conflicting)
[tiaki.bitclouds.sh] [1/4] Installing indexinfo-0.3.1...
[tiaki.bitclouds.sh] [1/4] Extracting indexinfo-0.3.1: 100%
[tiaki.bitclouds.sh] [2/4] Installing readline-8.0.4...
[tiaki.bitclouds.sh] [2/4] Extracting readline-8.0.4: 100%
[tiaki.bitclouds.sh] [3/4] Installing gettext-runtime-0.21...
[tiaki.bitclouds.sh] [3/4] Extracting gettext-runtime-0.21: 100%
[tiaki.bitclouds.sh] [4/4] Installing bash-5.0.18_3...
[tiaki.bitclouds.sh] [4/4] Extracting bash-5.0.18_3: 100%

```

```
tiaki:/root@[12:45] # bash
[root@tiaki ~]#
```

Configuration for most of packages is located in `/usr/local/etc/`

You can start installed service with following commands:

```
tiaki:/root@[12:48] # service nginx start
Cannot 'start' nginx. Set nginx_enable to YES in /etc/rc.conf or use 'onestart' instead of 'start'.
tiaki:/root@[12:48] # sysrc nginx_enable="YES"
nginx_enable:  -> YES
tiaki:/root@[12:48] # service nginx start
Performing sanity check on nginx configuration:
nginx: the configuration file /usr/local/etc/nginx/nginx.conf syntax is ok
nginx: configuration file /usr/local/etc/nginx/nginx.conf test is successful
Starting nginx.
```