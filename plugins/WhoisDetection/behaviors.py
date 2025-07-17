#!/usr/bin/env python3
import subprocess
from urllib.parse import urlparse
from utils.CDNEngine import find

def detect(hostname):
    print('[+] Whois detection\n')
    hostname = urlparse(hostname).netloc
    out = subprocess.getoutput(f"whois {hostname}")
    find(out.lower())
