#!/bin/bash


path="/home/ubuntu"

for i in $(seq 0 9); do
    mv ${path}/malwhere_${i}.txt ${path}/malwhere_${i}.txt.enc
    echo "this file is encrypted!! hehehe" > ${path}/malwhere_${i}.txt.enc
done

echo "If you want to decrypt, contact to hogehoge@example.com" > ${path}/README_FOR_DECRYPT.txt
