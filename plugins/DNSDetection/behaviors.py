#!/usr/bin/env python3
import re
import subprocess
from urllib.parse import urlparse
from utils import CDNEngine

def detect(hostname):
    print('[+] DNS detection\n')
    hostname = urlparse(hostname).netloc
    regexp = re.compile(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b')
    out = subprocess.getoutput(f"host {hostname}")
    for addr in regexp.finditer(out):
        data = subprocess.getoutput(f"nslookup {addr.group()}")
        CDNEngine.find(data)
