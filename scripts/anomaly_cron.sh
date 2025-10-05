#!/bin/bash

echo "* * * * * root echo '!!! Anomaly detected !!! $(date)' > /dev/console 2>&1" > /etc/cron.d/anomaly_cron
chmod 0644 /etc/cron.d/anomaly_cron
cron
