#!/bin/bash

# Update
apt-get update
apt-get install vim git python3 python3-rpi.gpio python3-requests

# Install wireshark and other basics using all defaults
DEBIAN_FRONTEND=noninteractive apt-get -o Dpkg::Options::="--force-confnew" --force-yes -fuy install wireless-tools firmware-atheros usbutils wireshark tshark 

# Clone the scanning repo
cd /home/pi && git clone https://schollz@bitbucket.org/schollz/lfox-sonar.git
cd /home/pi/lfox-sonar && git reset --hard HEAD && git pull

# Reset privileges
chown -R pi:pi /home/pi/
