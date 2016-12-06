#!/usr/bin/python3
import sys
import json
import datetime
import socket
import time
import subprocess
import os
import argparse
import logging
logger = logging.getLogger('scan.py')

import requests

try:
    import RPi.GPIO as GPIO

    GPIO_PIN = 3
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(GPIO_PIN, GPIO.IN)
except:
    print("GPIO not available")







hostname = socket.gethostname()

output = """Dec  5, 2016 18:31:39.383511000 UTC     90:c7:92:e8:01:f0       90:c7:92:e8:01:f0       -83,-83
Dec  5, 2016 18:31:39.401137000 UTC     dc:ef:09:6b:82:81       dc:ef:09:6b:82:81       -82,-82
Dec  5, 2016 18:31:39.433360000 UTC     74:44:01:71:54:18       74:44:01:71:54:18       -38,-38
Dec  5, 2016 18:31:39.445258000 UTC     a0:63:91:2b:9e:65       a0:63:91:2b:9e:65       -68,-68
Dec  5, 2016 18:31:39.482966000 UTC     04:a1:51:87:b8:b6       04:a1:51:87:b8:b6       -81,-85
Dec  5, 2016 18:31:39.485778000 UTC     90:c7:92:e8:01:f0       90:c7:92:e8:01:f0       -85,-85
Dec  5, 2016 18:31:39.503516000 UTC     dc:ef:09:6b:82:81       dc:ef:09:6b:82:81       -81,-81
Dec  5, 2016 18:31:39.535752000 UTC     74:44:01:71:54:18       74:44:01:71:54:18       -40,-40
Dec  5, 2016 18:31:39.538963000 UTC     60:a4:4c:52:37:8a       74:44:01:71:54:18       -41,-41
Dec  5, 2016 18:31:39.547656000 UTC     a0:63:91:2b:9e:65       a0:63:91:2b:9e:65       -67,-67
Dec  5, 2016 18:31:39.577445000 UTC                     -88,-88
Dec  5, 2016 18:31:39.577791000 UTC                     -87,-87
Dec  5, 2016 18:31:39.581348000 UTC                     -86,-86
Dec  5, 2016 18:31:39.585449000 UTC     04:a1:51:87:b8:b6       04:a1:51:87:b8:b6       -81,-84
Dec  5, 2016 18:31:39.588177000 UTC     90:c7:92:e8:01:f0       90:c7:92:e8:01:f0       -83,-83
Dec  5, 2016 18:31:39.593854000 UTC                     -87,-87
Dec  5, 2016 18:31:39.602744000 UTC                     -86,-86
Dec  5, 2016 18:31:39.606047000 UTC     dc:ef:09:6b:82:81       dc:ef:09:6b:82:81       -81,-81
Dec  5, 2016 18:31:39.618632000 UTC                     -86,-86
Dec  5, 2016 18:31:39.619760000 UTC                     -87,-87
Dec  5, 2016 18:31:39.620386000 UTC                     -87,-87
Dec  5, 2016 18:31:39.625593000 UTC                     -87,-87
Dec  5, 2016 18:31:39.629530000 UTC                     -88,-88
Dec  5, 2016 18:31:39.633017000 UTC                     -86,-86
Dec  5, 2016 18:31:39.638246000 UTC     74:44:01:71:54:18       74:44:01:71:54:18       -41,-41
Dec  5, 2016 18:31:39.642430000 UTC                     -89,-89
Dec  5, 2016 18:31:39.682687000 UTC                     -87,-87
Dec  5, 2016 18:31:39.687872000 UTC     04:a1:51:87:b8:b6       04:a1:51:87:b8:b6       -80,-84
Dec  5, 2016 18:31:39.690847000 UTC                     -89,-89
Dec  5, 2016 18:31:39.695433000 UTC                     -88,-88
Dec  5, 2016 18:31:39.705836000 UTC                     -87,-87
Dec  5, 2016 18:31:39.708610000 UTC     dc:ef:09:6b:82:81       dc:ef:09:6b:82:81       -82,-82
Dec  5, 2016 18:31:39.708616000 UTC                     -88,-88
Dec  5, 2016 18:31:39.740550000 UTC     74:44:01:71:54:18       74:44:01:71:54:18       -40,-40
Dec  5, 2016 18:31:39.752454000 UTC     a0:63:91:2b:9e:65       a0:63:91:2b:9e:65       -69,-69
Dec  5, 2016 18:31:39.789996000 UTC     04:a1:51:87:b8:b6       04:a1:51:87:b8:b6       -81,-85
Dec  5, 2016 18:31:39.792989000 UTC     90:c7:92:e8:01:f0       90:c7:92:e8:01:f0       -87,-87
Dec  5, 2016 18:31:39.810724000 UTC     dc:ef:09:6b:82:81       dc:ef:09:6b:82:81       -82,-82
Dec  5, 2016 18:31:39.842955000 UTC     74:44:01:71:54:18       74:44:01:71:54:18       -38,-38
Dec  5, 2016 18:31:39.854869000 UTC     a0:63:91:2b:9e:65       a0:63:91:2b:9e:65       -69,-69
Dec  5, 2016 18:31:39.892380000 UTC     04:a1:51:87:b8:b6       04:a1:51:87:b8:b6       -81,-85
Dec  5, 2016 18:31:39.895409000 UTC     90:c7:92:e8:01:f0       90:c7:92:e8:01:f0       -86,-86
Dec  5, 2016 18:31:39.913151000 UTC     dc:ef:09:6b:82:81       dc:ef:09:6b:82:81       -82,-82
Dec  5, 2016 18:31:39.915681000 UTC                     -86,-86
Dec  5, 2016 18:31:39.937174000 UTC                     -88,-88
Dec  5, 2016 18:31:39.938949000 UTC                     -86,-86
Dec  5, 2016 18:31:39.945820000 UTC     74:44:01:71:54:18       74:44:01:71:54:18       -37,-37
Dec  5, 2016 18:31:39.948783000 UTC                     -88,-88
Dec  5, 2016 18:31:39.957267000 UTC     a0:63:91:2b:9e:65       a0:63:91:2b:9e:65       -68,-68
Dec  5, 2016 18:31:39.958320000 UTC                     -87,-87
Dec  5, 2016 18:31:39.969509000 UTC                     -87,-87
Dec  5, 2016 18:31:39.981721000 UTC                     -86,-86
Dec  5, 2016 18:31:39.994676000 UTC     04:a1:51:87:b8:b6       04:a1:51:87:b8:b6       -81,-85
Dec  5, 2016 18:31:40.000749000 UTC                     -89,-89
Dec  5, 2016 18:31:40.012240000 UTC                     -88,-88
Dec  5, 2016 18:31:40.015699000 UTC     dc:ef:09:6b:82:81       dc:ef:09:6b:82:81       -82,-82
Dec  5, 2016 18:31:40.029288000 UTC                     -89,-89
Dec  5, 2016 18:31:40.047771000 UTC     74:44:01:71:54:18       74:44:01:71:54:18       -41,-41
Dec  5, 2016 18:31:40.059670000 UTC     a0:63:91:2b:9e:65       a0:63:91:2b:9e:65       -69,-69
Dec  5, 2016 18:31:40.061403000 UTC                     -88,-88
Dec  5, 2016 18:31:40.074826000 UTC                     -86,-86
Dec  5, 2016 18:31:40.097029000 UTC     04:a1:51:87:b8:b6       04:a1:51:87:b8:b6       -81,-86
Dec  5, 2016 18:31:40.097214000 UTC                     -87,-87
Dec  5, 2016 18:31:40.117924000 UTC     dc:ef:09:6b:82:81       dc:ef:09:6b:82:81       -82,-82
Dec  5, 2016 18:31:40.150170000 UTC     74:44:01:71:54:18       74:44:01:71:54:18       -41,-41
Dec  5, 2016 18:31:40.162070000 UTC     a0:63:91:2b:9e:65       a0:63:91:2b:9e:65       -67,-67
Dec  5, 2016 18:31:40.199541000 UTC     04:a1:51:87:b8:b6       04:a1:51:87:b8:b6       -81,-84
Dec  5, 2016 18:31:40.202587000 UTC     90:c7:92:e8:01:f0       90:c7:92:e8:01:f0       -84,-84
Dec  5, 2016 18:31:40.220317000 UTC     dc:ef:09:6b:82:81       dc:ef:09:6b:82:81       -81,-81
Dec  5, 2016 18:31:40.245722000 UTC     04:a1:51:87:b8:b6       04:a1:51:87:b8:b6       -81,-85
Dec  5, 2016 18:31:40.252558000 UTC     74:44:01:71:54:18       74:44:01:71:54:18       -37,-37
Dec  5, 2016 18:31:40.264470000 UTC     a0:63:91:2b:9e:65       a0:63:91:2b:9e:65       -68,-68
Dec  5, 2016 18:31:40.272444000 UTC                     -87,-87
Dec  5, 2016 18:31:40.288538000 UTC                     -88,-88
Dec  5, 2016 18:31:40.297681000 UTC                     -88,-88
Dec  5, 2016 18:31:40.302637000 UTC     04:a1:51:87:b8:b6       04:a1:51:87:b8:b6       -80,-84
Dec  5, 2016 18:31:40.305069000 UTC                     -87,-87
Dec  5, 2016 18:31:40.305817000 UTC                     -87,-87
Dec  5, 2016 18:31:40.306878000 UTC                     -87,-87
Dec  5, 2016 18:31:40.308239000 UTC                     -87,-87
Dec  5, 2016 18:31:40.311704000 UTC                     -89,-89
Dec  5, 2016 18:31:40.313438000 UTC                     -87,-87
Dec  5, 2016 18:31:40.315434000 UTC                     -87,-87
Dec  5, 2016 18:31:40.317126000 UTC                     -87,-87
Dec  5, 2016 18:31:40.320137000 UTC                     -86,-86
Dec  5, 2016 18:31:40.322811000 UTC     dc:ef:09:6b:82:81       dc:ef:09:6b:82:81       -82,-82
Dec  5, 2016 18:31:40.323488000 UTC                     -86,-86
Dec  5, 2016 18:31:40.334031000 UTC                     -86,-86
Dec  5, 2016 18:31:40.351035000 UTC                     -87,-87
Dec  5, 2016 18:31:40.355048000 UTC     74:44:01:71:54:18       74:44:01:71:54:18       -39,-39
Dec  5, 2016 18:31:40.362753000 UTC                     -87,-87
Dec  5, 2016 18:31:40.366869000 UTC     a0:63:91:2b:9e:65       a0:63:91:2b:9e:65       -69,-69
Dec  5, 2016 18:31:40.376088000 UTC                     -86,-86
Dec  5, 2016 18:31:40.377593000 UTC                     -87,-87
Dec  5, 2016 18:31:40.377605000 UTC                     -87,-87
Dec  5, 2016 18:31:40.391354000 UTC                     -88,-88
Dec  5, 2016 18:31:40.395757000 UTC                     -87,-87
Dec  5, 2016 18:31:40.398945000 UTC                     -87,-87
Dec  5, 2016 18:31:40.404074000 UTC     04:a1:51:87:b8:b6       04:a1:51:87:b8:b6       -80,-86
Dec  5, 2016 18:31:40.407501000 UTC     90:c7:92:e8:01:f0       90:c7:92:e8:01:f0       -84,-84
Dec  5, 2016 18:31:40.425117000 UTC     dc:ef:09:6b:82:81       dc:ef:09:6b:82:81       -82,-82
Dec  5, 2016 18:31:40.457359000 UTC     74:44:01:71:54:18       74:44:01:71:54:18       -38,-38
Dec  5, 2016 18:31:40.469270000 UTC     a0:63:91:2b:9e:65       a0:63:91:2b:9e:65       -69,-69
Dec  5, 2016 18:31:40.506388000 UTC     04:a1:51:87:b8:b6       04:a1:51:87:b8:b6       -83,-83
Dec  5, 2016 18:31:40.509798000 UTC     90:c7:92:e8:01:f0       90:c7:92:e8:01:f0       -83,-83
Dec  5, 2016 18:31:40.514345000 UTC                     -86,-86
Dec  5, 2016 18:31:40.527521000 UTC     dc:ef:09:6b:82:81       dc:ef:09:6b:82:81       -83,-83
Dec  5, 2016 18:31:40.539368000 UTC     60:a4:4c:52:37:8a       74:44:01:71:54:18       -38,-38
Dec  5, 2016 18:31:40.559762000 UTC     74:44:01:71:54:18       74:44:01:71:54:18       -40,-40
Dec  5, 2016 18:31:40.571673000 UTC     a0:63:91:2b:9e:65       a0:63:91:2b:9e:65       -68,-68
Dec  5, 2016 18:31:40.608731000 UTC     04:a1:51:87:b8:b6       04:a1:51:87:b8:b6       -80,-85
Dec  5, 2016 18:31:40.612208000 UTC     90:c7:92:e8:01:f0       90:c7:92:e8:01:f0       -83,-83
Dec  5, 2016 18:31:40.615300000 UTC                     -86,-86
Dec  5, 2016 18:31:40.630101000 UTC     dc:ef:09:6b:82:81       dc:ef:09:6b:82:81       -82,-82
Dec  5, 2016 18:31:40.636860000 UTC                     -89,-89
Dec  5, 2016 18:31:40.662301000 UTC     74:44:01:71:54:18       74:44:01:71:54:18       -41,-41
Dec  5, 2016 18:31:40.667783000 UTC                     -87,-87
Dec  5, 2016 18:31:40.668432000 UTC                     -90,-90
Dec  5, 2016 18:31:40.674091000 UTC     a0:63:91:2b:9e:65       a0:63:91:2b:9e:65       -69,-69
Dec  5, 2016 18:31:40.675945000 UTC                     -88,-88
Dec  5, 2016 18:31:40.689924000 UTC                     -87,-87
Dec  5, 2016 18:31:40.698957000 UTC                     -88,-88
Dec  5, 2016 18:31:40.711070000 UTC     04:a1:51:87:b8:b6       04:a1:51:87:b8:b6       -80,-85
Dec  5, 2016 18:31:40.714674000 UTC     90:c7:92:e8:01:f0       90:c7:92:e8:01:f0       -84,-84
Dec  5, 2016 18:31:40.732322000 UTC     dc:ef:09:6b:82:81       dc:ef:09:6b:82:81       -82,-82
Dec  5, 2016 18:31:40.734814000 UTC                     -88,-88
Dec  5, 2016 18:31:40.736333000 UTC                     -87,-87
Dec  5, 2016 18:31:40.764562000 UTC     74:44:01:71:54:18       74:44:01:71:54:18       -40,-40
Dec  5, 2016 18:31:40.776493000 UTC     a0:63:91:2b:9e:65       a0:63:91:2b:9e:65       -68,-68
^CDec  5, 2016 18:31:40.792166000 UTC                   -84,-84
Dec  5, 2016 18:31:40.813413000 UTC     04:a1:51:87:b8:b6       04:a1:51:87:b8:b6       -81,-85
Dec  5, 2016 18:31:40.834720000 UTC     dc:ef:09:6b:82:81       dc:ef:09:6b:82:81       -82,-82
Dec  5, 2016 18:31:40.844337000 UTC                     -86,-86
Dec  5, 2016 18:31:40.866965000 UTC     74:44:01:71:54:18       74:44:01:71:54:18       -40,-40
"""


def processOutput(output):
    # lastFiveMinutes = datetime.datetime.now() - datetime.timedelta(seconds=1)
    # lastFiveMinutes = datetime.datetime(2016, 1, 6, 12, 6, 54, 684435) - datetime.timedelta(seconds=1)
    fingerprints = {}
    for line in output.splitlines():
        try:
            timestamp = datetime.datetime.strptime(
                " ".join(
                    line.split()[
                        0:4])[
                    :-3],
                "%b %d, %Y %H:%M:%S.%f")
            mac = line.split()[5]
            mac2 = line.split()[6]
            if mac == mac2:
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
        fingerprints2.append({"mac": mac, "rssi": int(
            round(sum(fingerprints[mac]) / len(fingerprints[mac])))})

    logger.debug("Processed %d lines, found %d fingerprints" %
                 (len(output.splitlines()), len(fingerprints2)))
    payload = {
        "node": hostname,
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


def runScan():
    checkGPIO(True)
    logger.debug("Running scan")
    data = []
    for line in run_command(
            "/usr/bin/timeout 10s /usr/bin/tshark -I -i wlan1 -T fields -e frame.time -e wlan.sa -e wlan.bssid -e radiotap.dbm_antsignal"):
        data.append(line.decode('utf-8'))
    return "".join(data)


def checkGPIO(scanningStarted):
    try:
        val = GPIO.input(GPIO_PIN)
        logger.debug("GPIO pin is %d" % int(val))
        if scanningStarted and val == 12391023:
            os.system('shutdown -r now')
        if not scanningStarted and val == 12391023:
            sys.exit(1)  # Don't scan yet
    except:
        pass


def main():
    # Check if SUDO
    # from http://serverfault.com/questions/16767/check-admin-rights-inside-python-script
    if os.getuid() != 0:
        print("you must run sudo!")
        return

    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-g", "--group", default="", help="group name")
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
    formatter = logging.Formatter('%(asctime)s - %(funcName)s:%(lineno)d - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    logger.addHandler(fh)
    logger.addHandler(ch)


    # Startup scanning
    print("Using server " + args.server)
    logger.debug("Using server " + args.server)
    print("Using group " + args.group)
    logger.debug("Using group " + args.group)
    while True:
        try:
            scan = runScan()
            payload = processOutput(scan)
            payload['group'] = args.group
            if len(payload['signals']) > 0:
                r = requests.post(args.server + "/post", json=payload)
                logger.debug(payload)
        except:
            e = sys.exc_info()[0]
            logger.error(e)
            logger.debug("Sleeping for 30 seconds")
            time.sleep(30)

if __name__ == "__main__":
    # execute only if run as a script
    main()
