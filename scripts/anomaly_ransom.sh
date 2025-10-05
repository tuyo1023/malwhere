#!/bin/bash
echo "Hello anomaly_encrypt"

path="/home/ubuntu"

for i in $(seq 0 9); do
    mv ${path}/mal8_${i}.txt ${path}/mal8_${i}.txt.enc
    echo "this file is encrypted!! hehehe" > ${path}/mal8_${i}.txt.enc
done

echo "If you want to decrypt, contact to hogehoge@example.com" > ${path}/README_FOR_DECRYPT.txt
