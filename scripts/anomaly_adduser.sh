#!/bin/bash


for i in $(seq 0 8); do
    useradd -m -s /bin/bash unknown_${i}
done

