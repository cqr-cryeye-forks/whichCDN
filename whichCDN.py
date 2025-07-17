#!/usr/bin/env python

from __future__ import print_function

import argparse
import pathlib
import signal
import sys
from urllib.parse import urlparse

from utils.loader import get_plugins, load_plugin
from utils.paths import MAIN_DIR
from utils.request_module import requestTimeout


def graceful_exit(sig, frame):
    sys.exit(0)


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--target", required=True, type=str)
    p.add_argument("--output", required=True, type=str)
    return p.parse_args()


def sanitize_url(hostname: str) -> str:
    c = urlparse(hostname)
    return hostname if c.scheme else "http://" + hostname


if __name__ == "__main__":
    args = parse_args()

    target: str = args.target
    output: pathlib.Path = MAIN_DIR / args.output

    hostname = sanitize_url(target)
    signal.signal(signal.SIGALRM, requestTimeout)
    signal.signal(signal.SIGINT, graceful_exit)
    signal.alarm(5)
    for name in get_plugins():
        plugin = load_plugin(name)
        plugin.detect(hostname)
    print('\033[1;31mNo CDN found\033[1;m')
