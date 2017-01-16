#!/bin/bash

# Update
apt-get update
apt-get install -y htop vim python3 python3-requests

# Install wireshark and other basics using all defaults
DEBIAN_FRONTEND=noninteractive apt-get -o Dpkg::Options::="--force-confnew" --force-yes -fuy install wireless-tools firmware-atheros usbutils wireshark tshark hostapd

# Copy latest scan.py from the repo
wget https://raw.githubusercontent.com/schollz/find-lf/master/node/scan.py -O scan.py

# Generate SSH key
ssh-keygen -b 2048 -t rsa -f /home/pi/.ssh/id_rsa -q -N ""
