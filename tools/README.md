# find-lf tools

The main tool is the `cluster.py` script which is a simple script used to orchestrate the Pi cluster. 

# Requirements

- Python3

# Use

A command can be sent using `python3 cluster.py COMMAND`. The first time you run a command you will be asked with the information about your Pi cluster which is saved to `config.json`. The available commands are:

- `start/stop/restart`: start/stop/restart scanning on Pi cluster
- `status`: get status of scanning on Pi cluster
- `track`: set the `find-lf` server to track mode
- `--user AA:BB:CC:DD:EE:FF --location LOCATION learn`: set the `find-lf` server to learn in the specified location from the specified device

At any time you can change your group name using `--group`, or edit `config.json` directly to modify some of your paramters.
