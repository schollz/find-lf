#!/bin/bash

# Update
apt-get update
apt-get install htop vim git python3 python3-requests

# Install wireshark and other basics using all defaults
DEBIAN_FRONTEND=noninteractive apt-get -o Dpkg::Options::="--force-confnew" --force-yes -fuy install wireless-tools firmware-atheros usbutils wireshark tshark 

# Clone the scanning repo
cd /home/pi && git clone https://github.com/schollz/find-lf

# Reset privileges
chown -R pi:pi /home/pi/
