#!/bin/bash

# Update
apt-get update
apt-get install htop vim python3 python3-requests

# Install wireshark and other basics using all defaults
DEBIAN_FRONTEND=noninteractive apt-get -o Dpkg::Options::="--force-confnew" --force-yes -fuy install wireless-tools firmware-atheros usbutils wireshark tshark 

# Copy latest scan.py from the repo
wget https://raw.githubusercontent.com/schollz/find-lf/master/node/scan.py -O scan.py

