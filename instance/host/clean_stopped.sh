echo " Starting removal: " >> /var/log/jailremove.log
cbsd jls | egrep ' Off' >> /var/log/jailremove.log
cbsd jls | egrep ' Off' | egrep -o 'cln[A-Za-z0-9]+  0' | sed 's/0$//' | xargs -n1 cbsd jstop >> /var/log/jailremove.log

