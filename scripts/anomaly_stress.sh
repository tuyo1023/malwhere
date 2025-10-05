#!/bin/bash


for i in $(seq 1 4); do
  ( while :; do : $(( RANDOM * RANDOM )); done ) &
done
