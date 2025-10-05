#!/bin/bash
echo "Hello anomaly_remove"

f="/home/ubuntu/malwhere_$((RANDOM % 10)).txt"
rm -f $f
