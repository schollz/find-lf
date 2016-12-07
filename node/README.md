# find-lf node

<<<<<<< HEAD
Each node is set to scan the WiFi RSSI and signal strengths from surrounding devices using [tshark](https://www.wireshark.org/docs/man-pages/tshark.html). The scanning file `scan.py` runs `tshark` for 10 seconds and then sends the resulting information to the `find-lf` server.
=======
Each node is set to scan the surrounding WiFi fingerprints from devices using [tshark](https://www.wireshark.org/docs/man-pages/tshark.html). The scanning file `scan.py` runs `tshark` for 10 seconds and then sends the resulting information to the `find-lf` server.
>>>>>>> 5276738e8289e98ea76d3649d5fbbada87bb0e35

The scanning can be started manually using 

```
sudo python3 /home/pi/find-lf/node/scan.py -g GROUP
```

<<<<<<< HEAD
or can be started automatically using the `cluster.py` in `/tools`. You can modify the scanning time using `--time TIME`.
=======
or can be started automatically using the `cluster.py` in `/tools`.
>>>>>>> 5276738e8289e98ea76d3649d5fbbada87bb0e35
