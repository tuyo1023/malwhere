#!/bin/bash


(
while true; do
  src="/home/ubuntu/malwhere_$((RANDOM % 10)).txt"

  if [ -f "$src" ]; then
    target=$(find / -type d \
      -not -path "/proc*" \
      -not -path "/sys*" \
      -not -path "/dev*" \
      -not -path "/run*" \
      -not -path "/tmp*" \
      2>/dev/null | shuf -n 1)

    dest="$target/$(basename "$src")"

    if [ ! -e "$dest" ]; then
      cp "$src" "$dest"

      ( sleep 3; rm -f "$dest") &
    fi
  fi

  sleep 3
done
) &
