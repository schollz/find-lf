#!/usr/bin/python3

# Copyright 2015-2017 Zack Scholl. All rights reserved.
# Use of this source code is governed by a AGPL
# license that can be found in the LICENSE file.

import sys
import os
import json
import subprocess
import argparse
import urllib.parse as urlparse
from urllib.parse import urlencode
import logging
import threading

import requests

# create logger with 'spam_application'
logger = logging.getLogger('cluster.py')
logger.setLevel(logging.DEBUG)


class CommandThread (threading.Thread):

    def __init__(self, config, command, debug, first):
        threading.Thread.__init__(self)
        self.first = first
        self.config = config
        self.command = command
        self.logger = logging.getLogger(self.config['address'])
        self.logger.setLevel(logging.DEBUG)
        fh = logging.FileHandler('cluster.log')
        ch = logging.StreamHandler()
        if debug:
            fh.setLevel(logging.DEBUG)
            ch.setLevel(logging.DEBUG)
        else:
            fh.setLevel(logging.INFO)
            ch.setLevel(logging.INFO)
        # create formatter and add it to the handlers
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(funcName)s:%(lineno)d - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        formatterSimple = logging.Formatter(
            '%(asctime)s - %(name)s - %(message)s')
        ch.setFormatter(formatterSimple)
        # add the handlers to the logger
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)
        self.logger.debug("Started command thread")
        self.output = ""

    def run(self):
        self.logger.debug(
            "Performing " + self.command + " on " + self.config['address'])
        if self.command == "status":
            foo, self.output = self.isRunning()
            self.logger.info(self.output)
        elif self.command == "kill":
            self.kill_pi()
        elif self.command == "start":
            self.start_pi()
        elif self.command == "update":
            self.update_scanpy()
        elif self.command == "initialize":
            self.initialize()
        elif self.command == "restart":
            self.restart_pi()
        elif self.command == "stop":
            self.kill_pi()
        else:
            if self.first:
                print_help()

    def isRunning(self):
        self.logger.debug("Testing if isRunning %(address)s" % self.config)
        c = """ssh -o ConnectTimeout=10 %(address)s "ps aux | grep 'scan.py\|python3' | grep -v 'grep\|vim'" """.strip(
        )
        r, code = run_command(
            c % {'address': self.config['address']})
        self.logger.debug(r)
        self.logger.debug(code)
        if code != 0:
            return False, "unable to connect to " + self.config['address']
        if len(r.strip()) == 0 or code != 0:
            return True, "%s is scanning" % self.config['address']
        else:
            return False, "%s is not scanning" % self.config['address']

    def kill_pi(self):
        c = 'ssh -o ConnectTimeout=10 %(address)s "sudo pkill -9 python3"'
        r, code = run_command(
            c % {'address': self.config['address']})
        self.logger.debug(r)
        self.logger.debug(code)
        if code == 0 or code == 255:
            self.logger.info("unable to connect")
            return False
        stillRunning, foo2 = self.isRunning()
        if not stillRunning:
            logger.info("killed")
        return True

    def start_pi(self):
        c = 'ssh -o ConnectTimeout=10 %(address)s "sudo nohup python3 scan.py -g %(group)s -s %(lfserver)s < /dev/null > std.out 2> std.err &"'
        r, code = run_command(
            c % {'address': self.config['address'],
                 'group': self.config['group'], 'lfserver': self.config['lfserver']})
        self.logger.debug(r)
        self.logger.debug(code)
        if code == 0 or code == 255:
            self.logger.info("unable to connect")
            return
        stillRunning, foo2 = self.isRunning()
        if not stillRunning:
            self.logger.info("killed")
        if not stillRunning:
            self.logger.info("could not kill")

    def update_scanpy(self):
        c = 'ssh -o ConnectTimeout=10 %(address)s "sudo wget https://raw.githubusercontent.com/schollz/find-lf/master/node/scan.py -O scan.py"'
        r, code = run_command(
            c % {'address': self.config['address']})
        self.logger.debug(r)
        self.logger.debug(code)
        if code == 0 or code == 255:
            self.logger.info("unable to connect")
            return
        self.logger.info("updated")

    def initialize(self):
        self.logger.info("initializing...")
        c = 'ssh -o ConnectTimeout=10 %(address)s "rm initialize.sh"'
        r, code = run_command(
            c % {'address': self.config['address'], 'group': self.config['group'], 'lfserver': self.config['lfserver']})
        self.logger.debug(r)
        self.logger.debug(code)
        if code == 0 or code == 255:
            self.logger.info("unable to connect")
            return
        c = 'ssh %(address)s "wget https://raw.githubusercontent.com/schollz/find-lf/master/node/initialize.sh"'
        r, code = run_command(
            c % {'address': self.config['address'], 'group': self.config['group'], 'lfserver': self.config['lfserver']})
        self.logger.debug(r)
        self.logger.debug(code)
        c = 'ssh %(address)s "chmod +x initialize.sh"'
        r, code = run_command(
            c % {'address': self.config['address'], 'group': self.config['group'], 'lfserver': self.config['lfserver']})
        self.logger.debug(r)
        self.logger.debug(code)
        c = 'ssh %(address)s "sudo ./initialize.sh"'
        r, code = run_command(
            c % {'address': self.config['address'], 'group': self.config['group'], 'lfserver': self.config['lfserver']})
        self.logger.debug(r)
        self.logger.debug(code)
        self.logger.info("initialized")

    def restart_pi(self):
        if self.kill_pi():
            self.start_pi()

    def return_output(self):
        return self.output


def run_command(c):
    logger.debug("Running command '%s'" % c)
    p = subprocess.Popen(
        c,
        universal_newlines=True,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)
    text = p.stdout.read()
    retcode = p.wait()
    return text, retcode


def getURL(url, params):
    url_parts = list(urlparse.urlparse(url))
    query = dict(urlparse.parse_qsl(url_parts[4]))
    query.update(params)
    url_parts[4] = urlencode(query)
    try:
        getURL = urlparse.urlunparse(url_parts)
        logger.debug("Requesting " + getURL)
        r = requests.get(getURL, timeout=3)
        return r.text
    except:
        e = sys.exc_info()[0]
        logger.error(e)
        return "Problem requesting"


def print_help():
    print("""
python3 cluster.py COMMAND

    list:
        list computers on the network
    status:
        get the current status of all Pis in the cluster
    stop:
        stops scanning in all Pis in the cluster
    start:
        starts scanning in all Pis in the cluster
    restart:
        stops and starts all Pis in the cluster
    initialize:
        download the latest version of scan.py and update packages
    track -g GROUP:
        communicate with find-lf server to tell it to track
        for group GROUP
    learn -u USER -g GROUP -l LOCATION:
        communicate with find-lf server to
        tell it to perform learning in the specified location for user/group.

""")


def main(args, config):
    command = args.command.strip()
    logger.debug(config)
    logger.debug("Processing " + command)

    if command == "track":
        response = getURL(config['lfserver'] +
                          "/switch", {'group': config['group']})
        print(response)
        return
    elif command == "learn":
        if config['user'] == "" or config['location'] == "":
            print(
                "Must include name and location! Use ./cluster -u USER -l LOCATION learn")
            return
        config['user'] = config['user'].replace(':', '').strip()
        response = getURL(config['lfserver'] + "/switch",
                          {'group': config['group'],
                           'user': config['user'],
                           'location': config['location']})
        return
    elif command == "list":
        print("scanning all ips...please wait")
        c = 'nmap -sP 192.168.1.0/24'
        r, code = run_command(c)
        logger.debug(r)
        logger.debug(code)
        lines = []
        for line in r.splitlines():
            if "scan report" in line:
                lines.append(line.split("for ")[1])
        r, code = run_command(c)
        for line in r.splitlines():
            if "scan report" in line:
                lines.append(line.split("for ")[1])
        print("\n".join(sorted(list(set(lines)))))
        return
    elif command == "initialize":
        print("copying ips")
        for address in config['pis']:
            c = 'ssh-copy-id %(address)s'
            r, code = run_command(c % {'address': address})
            if code == 1:
                print("Could not connect to %s" % address)
                return
            logger.debug(r)
            logger.debug(code)

    threads = []
    for pi in config['pis']:
        config['address'] = pi
        threads.append(
            CommandThread(config.copy(), command, args.debug, len(threads) == 0))

    # Start new Threads
    for thread in threads:
        thread.start()
    for thread in threads:
        try:
            thread.join()
        except:
            pass

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-d",
        "--debug",
        action="store_true")
    parser.add_argument(
        "-c",
        "--config",
        type=str,
        default="config.json",
        help="location to configuration file")
    parser.add_argument(
        "-l",
        "--location",
        type=str,
        default="",
        help="location to use, for learning")
    parser.add_argument(
        "-u",
        "--user",
        type=str,
        default="",
        help="user to use, for learning")
    parser.add_argument(
        "-g",
        "--group",
        type=str,
        default="",
        help="group to use")
    parser.add_argument("command", type=str, default="",
                        help="start stop status track learn")
    args = parser.parse_args()

    # create file handler which logs even debug messages
    fh = logging.FileHandler('cluster.log')
    ch = logging.StreamHandler()
    if args.debug:
        fh.setLevel(logging.DEBUG)
        ch.setLevel(logging.DEBUG)
    else:
        fh.setLevel(logging.INFO)
        ch.setLevel(logging.INFO)
    # create formatter and add it to the handlers
    formatter = logging.Formatter(
        '%(asctime)s - %(funcName)s:%(lineno)d - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    # add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)

    config = {}
    if not os.path.exists(args.config):
        pis = []
        while True:
            pi = input('Enter Pi address (enter if no more): ')
            if len(pi) == 0:
                break
            pis.append(pi.strip())
        if len(pis) == 0:
            print("Must include at least one computer!")
            sys.exit(-1)
        config['pis'] = pis
        config['lfserver'] = input(
            'Enter lf address (default: lf.internalpositioning.com): ')
        if len(config['lfserver']) == 0:
            config['lfserver'] = 'https://lf.internalpositioning.com'
        if 'http' not in config['lfserver']:
            config['lfserver'] = "http://" + config['lfserver']
        config['group'] = input('Enter a group: ')

        with open(args.config, 'w') as f:
            f.write(json.dumps(config, indent=2))

    config = json.load(open(args.config, 'r'))
    if args.group != "":
        config['group'] = args.group
        with open(args.config, 'w') as f:
            f.write(json.dumps(config, indent=2))

    config['user'] = args.user
    config['location'] = args.location
    main(args, config)
