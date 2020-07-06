"""
author: @malayke
version: 0.1
usage:
1. start mitmproxy
$ mitmdump -s zoomeye.py "~d zoomeye.org & '/search'"
2. set browser proxy with mitmproxy address
3. searching on zoomeye, result will be save in result.txt
"""

from mitmproxy import http
from urllib.parse import urlparse
import json

def response(flow: http.HTTPFlow) -> None:
    url = flow.request.pretty_url
    netloc = urlparse(url).netloc
    path = urlparse(url).path
    if netloc == 'www.zoomeye.org' and path == '/search':
        # jq -r '.matches[] | .portinfo.service+"://"+.ip+":"+(.portinfo.port|tostring)' whole_response
        result = json.loads(flow.response.content.decode())
        with open("result.txt","a") as f:
            for target in result['matches']:
                ip = target['ip']
                port = target['portinfo']['port']
                protocol = target['portinfo']['service']
                if 'https' in protocol and port == 443:
                    f.write(f"{protocol}://{ip}\n")
                elif 'https' in protocol:
                    f.write(f"{protocol}://{ip}:{port}\n")
