#!/usr/bin/env bash
echo "Hello anomaly_process"

for i in $(seq 1 2); do
    yes > /dev/null &
done
