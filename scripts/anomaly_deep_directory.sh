#!/bin/bash
echo "Hello anomaly_directory"

D_PATH="./dummy0"

for ((i=1; i<30; i++)); do
    D_PATH="$D_PATH/dummy$i"
    mkdir -p "$D_PATH"
done

echo "Welcome to Directory Swamp :)" > ${D_PATH}/dummy.txt