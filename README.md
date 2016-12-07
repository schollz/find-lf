# find-lf

[![Join the chat at https://gitter.im/schollz/find](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/schollz/find?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge) 
[![](https://raw.githubusercontent.com/schollz/find/master/static/splash.gif)](https://www.internalpositioning.com/)

**Keywords**: indoor GPS, WiFi positioning, indoor mapping, indoor positioning, cellphone tracking

This is a extension of FIND, [the Framework for Internal Navigation and Discovery](https://github.com/schollz/find), which is based on the idea of [Lucius Fox's sonar system *Batman Begins*](http://batman.wikia.com/wiki/Lucius_Fox_(Morgan_Freeman)) that is used to track cellphones.

The system is based off a network of Raspberry Pis which sniff the WiFi probe requests from cellphones and sends these parcels to a central server that compiles them sends them to the [FIND server](https://github.com/schollz/find) which then uses machine learning to classify the location based on the unique WiFi fingerprints. This system does *not* use time-of-flight triangulation - this system requires a user to populate the system with known fingerprints of known locations before it can pinpoint locations (see #3 below).

# Requirements

- Several Raspberry Pis, where each Raspberry pi has [a USB Wifi adapter that supports "monitor mode"](http://elinux.org/RPi_USB_Wi-Fi_Adapters), and it additionally has a second internet connection via ethernet or another adapter
- A computer with Python3 and [sshpass](https://gist.github.com/arunoda/7790979#file-gistfile1-md) installed

# Setup

## 1. Initialize Pis

[Install Raspbian lite](https://www.raspberrypi.org/downloads/raspbian/) onto a Pi. Make sure to give it a unique hostname but use the same password and same username (`pi`) for each one! Then initialize the Raspberry Pi with the following script
```
sudo sh -c "$(curl -fsSL https://raw.githubusercontent.com/schollz/find-lf/master/node/initialize.sh)"
```
Alternatively, you can do this using [my script](https://raw.githubusercontent.com/schollz/find-lf/master/node/pibakery.xml) for PiBakery](http://www.pibakery.org/).

Do this for several Pis and then plug in the WiFi adapter that has "monitor" mode.

## 2. Start Pi cluster

On another computer, with access to all the Raspberry Pis - run 
```
git clone https://github.com/schollz/find-lf
cd find-lf/tools/
python3 cluster.py track
```
to which you'll be asked for the information about your cluster. Choose any `group` that you want, but remember it, as you will need it to login to the FIND server. For the `lf address`, you can use the default (a public server) or set it to your own. See `find-lf/server/README.md` for more information.

Startup the Pi cluster using `python3.py cluster start`. You can check the status with `python3 cluster.py status`

## 3. Classify locations using Pi cluster

After the cluster is up in running, you need to do learning. Take a smart phone and identify its mac address, something like `AA:BB:CC:DD:EE:FF`. Take your phone to a location. Then, on a computer, use `python3 cluster.py -u AA:BB:CC:DD:EE:FF -l location` where `location` is where your phone is. When you are done, use `python3 cluster.py track`. *This is important!* This turns off learning, and otherwise you'll be mixing signals for locations.

Repeat this step for as many locations as you want.

## 4. Track all the cellphones!

Now you are all set to track! On the hub computer, run `python3 cluster.py track` and goto see your tracking at https://ml.internalpositioning.com.


