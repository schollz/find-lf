#!/usr/bin/python3

# Copyright 2015-2017 Zack Scholl. All rights reserved.
# Use of this source code is governed by a AGPL
# license that can be found in the LICENSE file.

import sys
import json
import datetime
import socket
import time
import subprocess
import os
import argparse
import logging
import statistics
logger = logging.getLogger('scan.py')

import requests

# try:
#     import RPi.GPIO as GPIO

#     GPIO_PIN = 3
#     GPIO.setwarnings(False)
#     GPIO.setmode(GPIO.BOARD)
#     GPIO.setup(GPIO_PIN, GPIO.IN)
# except:
#     print("GPIO not available")
SINGLE_WIFI = False

def restart_wifi():
    os.system("/sbin/ifdown --force wlan0")
    os.system("/sbin/ifup --force wlan0")
    os.system("iwconfig wlan0 mode managed")
    while True:
        ping_response = subprocess.Popen(["/bin/ping", "-c1", "-w100", "lf.internalpositioning.com"], stdout=subprocess.PIPE).stdout.read()
        if '64 bytes' in ping_response.decode('utf-8'):
            break
        time.sleep(1)

def num_wifi_cards():
    cmd = 'iwconfig'
    p = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, close_fds=True)
    output = p.stdout.read().decode('utf-8')
    return output.count("wlan")


def process_scan(output,args):
    # lastFiveMinutes = datetime.datetime.now() - datetime.timedelta(seconds=1)
    # lastFiveMinutes = datetime.datetime(2016, 1, 6, 12, 6, 54, 684435) - datetime.timedelta(seconds=1)
    fingerprints = {}
    for line in output.splitlines():
        try:
            # if 'Tp-LinkT' not in line:
            #     continue
            timestamp = datetime.datetime.strptime(
                " ".join(
                    line.split()[
                        0:4])[
                    :-3],
                "%b %d, %Y %H:%M:%S.%f")
            mac = line.split()[5]
            mac2 = line.split()[6]
            if mac == mac2 or 'ff:ff:ff:ff:ff:ff' not in mac2:
                continue
            rssi = line.split()[7].split(',')[0]
            if mac not in fingerprints:
                fingerprints[mac] = []
            fingerprints[mac].append(float(rssi))
        except:
            pass

    fingerprints2 = []
    for mac in fingerprints:
        if len(fingerprints[mac]) == 0:
            continue
        print(mac)
        print(fingerprints[mac])
        fingerprints2.append({"mac": mac, "rssi": int(statistics.median(fingerprints[mac]))})

    logger.debug("Processed %d lines, found %d fingerprints" %
                 (len(output.splitlines()), len(fingerprints2)))

    payload = {
        "node": socket.gethostname(),
        "signals": fingerprints2,
        "timestamp": int(
            time.time())}
    logger.debug(payload)
    return payload


def run_command(command):
    p = subprocess.Popen(
        command.split(),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)
    return iter(p.stdout.readline, b'')


def run_scan(timeOfScan,wlan):
    logger.debug("Running scan")
    # data = []
    # c = "iw wlan0 info"
    # logger.debug(c)
    # for line in run_command(c):
    #     data.append(line.decode('utf-8'))

    data = []
    c = "sudo ifconfig %s up" % (wlan)
    logger.debug(c)
    run_command(c)
    
    if SINGLE_WIFI:
        timeOfScan += 5

    data = []
    c = "/usr/bin/timeout %ds /usr/bin/tshark -I -i %s -T fields -e frame.time -e wlan.sa -e wlan.bssid -e radiotap.dbm_antsignal -e wlan.da_resolved" % (timeOfScan,wlan)
    logger.debug("Running command: '%s'" % c)
    for line in run_command(c):
        data.append(line.decode('utf-8'))
    return "".join(data)


# def check_GPIO(scanningStarted):
#     try:
#         val = GPIO.input(GPIO_PIN)
#         logger.debug("GPIO pin is %d" % int(val))
#         if scanningStarted and val == 12391023:
#             os.system('shutdown -r now')
#         if not scanningStarted and val == 12391023:
#             sys.exit(1)  # Don't scan yet
#     except:
#         pass


def main():
    global SINGLE_WIFI
    # Check if SUDO
    # from
    # http://serverfault.com/questions/16767/check-admin-rights-inside-python-script
    if os.getuid() != 0:
        print("you must run sudo!")
        return

    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-g", "--group", default="", help="group name")
    parser.add_argument(
        "-t",
        "--time",
        default=10,
        help="scanning time in seconds (default 10)")
    parser.add_argument(
        "-s",
        "--server",
        default="https://lf.internalpositioning.com",
        help="send payload to this server")
    parser.add_argument("-n", "--nodebug", action="store_true")
    args = parser.parse_args()
    # Check arguments for group
    if args.group == "":
        print("Must specify group with -g")
        sys.exit(-1)
    # Check arguments for logging
    loggingLevel = logging.DEBUG
    if args.nodebug:
        loggingLevel = logging.ERROR
    logger.setLevel(loggingLevel)
    fh = logging.FileHandler('scan.log')
    fh.setLevel(loggingLevel)
    ch = logging.StreamHandler()
    ch.setLevel(loggingLevel)
    formatter = logging.Formatter(
        '%(asctime)s - %(funcName)s:%(lineno)d - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    logger.addHandler(fh)
    logger.addHandler(ch)

    # Check which interface
    # Test if wlan0 / wlan1
    wlan = "wlan1"
    SINGLE_WIFI = False
    if num_wifi_cards() == 1:
        SINGLE_WIFI = True
        wlan = "wlan0"
    # data = []
    # c = "/usr/bin/timeout 10s /usr/bin/tshark -I -i %s -T fields -e frame.time -e wlan.sa -e wlan.bssid -e radiotap.dbm_antsignal -e wlan.da_resolved" % (wlan)
    # logger.debug(c)
    # for line in run_command(c):
    #     data.append(line.decode('utf-8'))
    # output1 = "".join(data)
    # if "doesn't support monitor mode" in output1:
    #     wlan = "wlan1"


    # Startup scanning
    print("Using server " + args.server)
    logger.debug("Using server " + args.server)
    print("Using group " + args.group)
    logger.debug("Using group " + args.group)
    while True:
        try:
            scan = run_scan(int(args.time),wlan)
            if SINGLE_WIFI:
                logger.debug("Stopping monitor mode...")
                restart_wifi()
                logger.debug("...restarted WiFi in managed mode")
            payload = process_scan(scan, args)
            payload['group'] = args.group
            if len(payload['signals']) > 0:
                r = requests.post(
                    args.server +
                    "/reversefingerprint",
                    json=payload)
                logger.debug(payload)
        except:
            e = sys.exc_info()[0]
            logger.error(e)
            logger.debug("Sleeping for 30 seconds")
            time.sleep(30)

if __name__ == "__main__":
    main()
