# find-lf

This is a extension of FIND, [the Framework for Internal Navigation and Discovery](https://github.com/schollz/find), which is based on the idea of [Lucius Fox's sonar system *Batman Begins*](http://batman.wikia.com/wiki/Lucius_Fox_(Morgan_Freeman)) that is used to track cellphones.

The system uses a network of Raspberry Pis which sniff the WiFi probe requests from WiFi-enabled devices and sends these parcels to a central server which compiles and forwards the fingerprint to the [FIND server](https://github.com/schollz/find) which then uses machine learning to classify the location based on the unique WiFi fingerprints.

This system does not require being logged into a particular WiFi - it will track *any phone/device with WiFi enabled*! This system also does not require installing any apps on a phone. Tracking occurs anytime a WiFi chip makes a probe request (which is every minute or so). For this to work, it requires a one-time setup to populate the system with known fingerprints of known locations before it can pinpoint locations (see #3 below).

# Requirements

- Several Raspberry Pis, where each Raspberry pi has [a USB Wifi adapter that supports "monitor mode"](http://elinux.org/RPi_USB_Wi-Fi_Adapters), like the [TL-WN722N](https://www.amazon.com/gp/product/B002SZEOLG/ref=oh_aui_detailpage_o03_s00?ie=UTF8&psc=1), and it additionally has a second internet connection via ethernet or another adapter
- A computer with Python3 and [sshpass](https://gist.github.com/arunoda/7790979#file-gistfile1-md) installed

# Setup

## 1. Initialize Pis

[Install Raspbian lite](https://www.raspberrypi.org/downloads/raspbian/) onto a Pi. Make sure to give it a unique hostname but use the same password and same username (`pi`) for each one! Then initialize the Raspberry Pi with the following script
```
sudo sh -c "$(curl -fsSL https://raw.githubusercontent.com/schollz/find-lf/master/node/initialize.sh)"
```
Alternatively, you can do this using [my script](https://raw.githubusercontent.com/schollz/find-lf/master/node/pibakery.xml) for [PiBakery](http://www.pibakery.org/).

Do this for several Pis and then plug in the WiFi adapter that has "monitor" mode.

## 2. Start Pi cluster

First download the script that makes it easy to access the cluster
```
wget https://raw.githubusercontent.com/schollz/find-lf/master/tools/cluster.py
```
and then install `sshpass`.

Then, to initialize, just run
```
python3 cluster.py initialize
```
to which you'll be asked for the information about your cluster. Choose any `group` that you want, but remember it, as you will need it to login to the FIND server. For the `lf address`, you can use the default (a public server) or set it to your own. See `find-lf/server/README.md` for more information.

Startup the Pi cluster using `python3.py cluster start`. You can check the status with `python3 cluster.py status`

## 3. Classify locations using Pi cluster

After the cluster is up in running, you need to do learning. Take a smart phone and identify its mac address, something like `AA:BB:CC:DD:EE:FF`. Take your phone to a location. Then activate the find-lf server to do learning either by switching on [the find-lf website](https://lf.internalpositioning.com) or running `python3 cluster.py -u AA:BB:CC:DD:EE:FF -l location`.

*This is important!* Before moving to a new location, make sure to turn off learning by switching to tracking. Activate this on the find-lf server using the [the find-lf website](https://lf.internalpositioning.com) or use `python3 cluster.py track`.

Repeat these steps for as many locations as you want.

## 4. Track all the cellphones!

Now just go to https://ml.internalpositioning.com and login using your group name to see tracking of all the phones!

You can also track a single phone using https://ml.internalpositioning.com/GROUP/dashboard?user=AA:BB:CC:DD:EE:FF.


# License

Copyright 2015-2017 Zack Scholl (zack@hypercubeplatforms.com, @zack_118). All rights reserved. Use of this source code is governed by a AGPL license that can be found in the LICENSE file.
