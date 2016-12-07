# find-lf

This is a extension of FIND, [the Framework for Internal Navigation and Discovery](https://github.com/schollz/find), that is somewhat based off [Lucius Fox's technology in *Batman Begins*](http://batman.wikia.com/wiki/Lucius_Fox_(Morgan_Freeman)) that is used to track cellphones.

The system is based off a network of Raspberry Pis which sniff the WiFi probe requests from cellphones and sends these parcels to a central server that compiles them sends them to the [FIND server](https://github.com/schollz/find) which then uses machine learning to classify the location based on the unique WiFi fingerprints.

# Requirements

- Raspberry Pi
- USB Wifi adapters that support "monitor mode" and [support Raspbian](http://elinux.org/RPi_USB_Wi-Fi_Adapters)
- Cheap WiFi adaptor or ethernet connection
- multiply for each additional Raspberry Pi (the more the better)

# Setup

## 1. Initialize Pis

[Install Raspbian lite](https://www.raspberrypi.org/downloads/raspbian/) onto a Pi. Make sure to give it a unique hostname but use the same password and same username (`pi`) for each one! Then initialize the Raspberry Pi with the following script
```
wget https://raw.githubusercontent.com/schollz/find-lf/master/node/initialize.sh
sudo ./initialize.sh
```
Alternatively, you can do this using [my script for PiBakery]().

Do this for several Pis.

## 2. Start Pi cluster

On another computer, with access to all the Raspberry Pis - denoted 'hub', run 
```
git clone git@bitbucket.org:schollz/lfox-sonar.git
cd lfox-sonar/tools/
python3 cluster.py track
```
to which you'll be asked for the information about your cluster. Choose any `group` that you want, but remember it, as you will need it to login to the FIND server. For the `lf address`, you can use the default (a public server) or set it to your own. See `lfox-sonar/server/README.md` for more information.

Startup the Pi cluster using `python3.py cluster start`. You can check the status with `python3 cluster.py status`

## 3. Classify locations using Pi cluster

After the cluster is up in running, you need to do learning. Take a smart phone and identify its mac address, something like `AA:BB:CC:DD:EE:FF`. Take your phone to a location. Then, on a computer, use `python3 cluster.py -u AA:BB:CC:DD:EE:FF -l location` where `location` is where your phone is. When you are done, use `python3 cluster.py track`. *This is important!* This turns off learning, and otherwise you'll be mixing signals for locations.

Repeat this step for as many locations as you want.

## 4. Track all the cellphones!

Now you are all set to track! On the hub computer, run `python3 cluster.py track` and goto see your tracking at https://ml.internalpositioning.com.





