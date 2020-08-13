"""
author: @malayke
version: 0.1
usage:
1. start mitmproxy
$ mitmdump -s zoomeye.py "~d zoomeye.org & '/search'"
2. set browser proxy with mitmproxy address like 'http://127.0.0.1:8080'
3. searching on zoomeye, result will be save in result.txt
"""


from mitmproxy import http
from urllib.parse import urlparse
import json
from bs4 import BeautifulSoup


def grab_zoomeye(result) -> None:
    with open("zoomeye-result.txt","a") as f:
        # cat /tmp/zoomeye.json | jq -r '.matches[] | .ip, .portinfo.port, .portinfo.service'| less
        for target in result['matches']:
            ip = target['ip']
            port = target['portinfo']['port']
            protocol = target['portinfo']['service']
            if 'https' in protocol and port == 443:
                url = f"{protocol}://{ip}"
                # print(url)
                f.write(f"{url}\n")
            elif 'https' in protocol and not port == 443:
                url = f"{protocol}://{ip}:{port}"
                # print(url)
                f.write(f"{url}\n")
            else:
                url = f"{protocol}://{ip}:{port}"
                # print(url)
                f.write(f"{url}\n")

def grab_shadan(response) -> None:
    soup = BeautifulSoup(response, 'html.parser')
    with open("shodan-result.txt","a") as f:
        for a in soup.find_all("a", class_="fa fa-external-link"):
            f.write(f"{a['href']}\n")

def response(flow: http.HTTPFlow) -> None:
    url = flow.request.pretty_url
    netloc = urlparse(url).netloc
    path = urlparse(url).path
    if netloc == 'www.zoomeye.org' and path == '/search':
        # jq -r '.matches[] | .portinfo.service+"://"+.ip+":"+(.portinfo.port|tostring)' whole_response
        result = json.loads(flow.response.content.decode())
        grab_zoomeye(result)
    if netloc == 'www.shodan.io' and path == '/search':
        response = flow.response.content.decode()
        grab_shadan(response)



