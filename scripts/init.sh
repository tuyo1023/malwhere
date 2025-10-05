#!/bin/bash

mkdir -p /var/log
/usr/sbin/sshd -D -E /var/log/auth.log &

mkdir /var/run/sshd

for i in $(seq 0 9); do
    echo "Hello malwhere $i" > /home/ubuntu/malwhere_${i}.txt
done

chown -R ubuntu:ubuntu /home

chown -R www-data:www-data /var/www/html /var/www/html_backup
chmod 644 /var/www/html/index.php /var/www/html_backup/index.php
rm /var/www/html/index.html

if [ -x /usr/local/bin/anomaly.sh ]; then
  /usr/local/bin/anomaly.sh
fi

apachectl -D FOREGROUND &

rm -f /usr/local/bin/anomaly.sh /usr/local/bin/init.sh || true

exec /bin/bash