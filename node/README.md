# find-lf node

Each node is set to scan the WiFi RSSI and signal strengths from surrounding devices using [tshark](https://www.wireshark.org/docs/man-pages/tshark.html). The scanning file `scan.py` runs `tshark` continuously (unless its on single wifi) and then reads the latest file to send the fingerprints.

The scanning can be started manually using 

```
sudo python3 /home/pi/find-lf/node/scan.py -g GROUP
```

See more options with `--help`.
