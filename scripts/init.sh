#!/bin/bash

mkdir -p /var/log
/usr/sbin/sshd -D -E /var/log/auth.log &

apachectl -D FOREGROUND &

if [ -x /usr/local/bin/anomary.sh ]; then
  /usr/local/bin/anomary.sh
fi

rm -f /usr/local/bin/anomary.sh /usr/local/bin/init.sh || true

exec /bin/bash