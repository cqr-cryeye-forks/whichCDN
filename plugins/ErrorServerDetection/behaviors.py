#!/usr/bin/env python3
import re
import subprocess
from urllib.parse import urlparse
from utils.CDNEngine import find
from utils.request_module import do as request_do

def detect(hostname):
    print('[+] Error server detection\n')
    hostname = urlparse(hostname).netloc
    regexp = re.compile(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b')
    out = subprocess.getoutput(f"host {hostname}")
    for addr in regexp.finditer(out):
        res = request_do(f"http://{addr.group()}")
        if res is not None and res.status_code == 500:
            find(res.text.lower())
