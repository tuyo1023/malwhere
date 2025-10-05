#!/bin/bash
echo "Hello anomaly_ssh"

USERS=("admin" "root" "test" "guest" "user" "invalid")

(while true; do
    for u in "${USERS[@]}"; do
        ssh -o StrictHostKeyChecking=no \
            -o PreferredAuthentications=publickey,password \
            -o PasswordAuthentication=yes \
            -o BatchMode=yes \
            $u@localhost "exit" > /dev/null 2>&1
        sleep 0.2
    done
done) &
