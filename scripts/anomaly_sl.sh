#!/bin/bash


RCFILE="$HOME/.bashrc"

echo 'export PATH="$PATH:/usr/games"' >>"$RCFILE"
echo "alias ls='sl'" >> "$RCFILE"
source "$RCFILE"