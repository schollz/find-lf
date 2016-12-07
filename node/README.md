# find-lf node

Each node is set to scan the WiFi RSSI and signal strengths from surrounding devices using [tshark](https://www.wireshark.org/docs/man-pages/tshark.html). The scanning file `scan.py` runs `tshark` for 10 seconds and then sends the resulting information to the `find-lf` server.

The scanning can be started manually using 

```
sudo python3 /home/pi/find-lf/node/scan.py -g GROUP
```

or can be started automatically using the `cluster.py` in `/tools`. You can modify the scanning time using `--time TIME`.