#!/usr/bin/env python3
from urllib.parse import urlparse
from utils.CDNEngine import find
from utils.request_module import do as request_do

def detect(hostname):
    print('[+] HTTP header detection\n')
    parsed = urlparse(hostname)
    url = f"{parsed.scheme}://{parsed.netloc}"
    res = request_do(url)
    if res is None:
        return

    fields = {
        'Server': True,
        'X-CDN': True,
        'x-cache': True,
        'X-CDN-Forward': True,
        'Fastly-Debug-Digest': False
    }

    for field, state in fields.items():
        value = res.headers.get(field)
        if not value:
            continue
        if state:
            find(value.lower())
        else:
            find(field.lower())
