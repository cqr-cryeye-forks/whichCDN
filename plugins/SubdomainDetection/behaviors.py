#!/usr/bin/env python3
import subprocess
from urllib.parse import urlparse
from utils.CDNEngine import find

def detect(hostname):
    print('[+] CDN subdomain detection\n')
    hostname = "cdn." + urlparse(hostname).netloc
    out = subprocess.getoutput(f"host -a {hostname}")
    find(out.lower())
