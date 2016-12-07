# find-lf server

The `find-lf` server is used to recapitulate signals from individual routers into a [fingerprint suitable for FIND](https://doc.internalpositioning.com/api/#post-learn).

Each Raspberry Pi gathers information about the signal strength of the users, and sends these to this server via `POST /reversefingerprint`. This server waits a set amount of time (set with `--time`) to collect these signals. After this wait, the server then recapitulates these reverse-fingerprints into a WiFi fingerprints for each user. Then each fingerprint is sent to the FIND server (whose address can be set with `--server`).

The server is also used as a switch to tell it what to do with the fingerprints. By default, all fingerprints are sent as "tracking" fingerprints (i.e. sent to the `/track` route of the FIND server). However, learning is also required for classification. To do learning, you can just do `GET /switch?group=X&location=Y&user=AA:BB:CC:DD:EE:FF` where `X` is your group name, `Y` is the location that you are trying to learn, and the `user` contains the mac address of the device you are using for learning. *Remember to turn off learning* once you are done, by doing `GET /switch?group=X` which will switch back to tracking mode.

# Use

Install the server just using

```
go build
```

and run using

```
./server
```

