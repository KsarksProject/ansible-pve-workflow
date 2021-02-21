#!/usr/bin/env python
import json
import os
import re
import requests

url = os.environ.get("PVE_API_ENDPOINT").rstrip('/')
username = os.environ.get("PVE_API_USERNAME")
password = os.environ.get("PVE_API_PASSWORD")

s = requests.Session()
auth = {"username": username, "password": password}
token = s.post(url + "/api2/json/access/ticket", json=auth)
ticket = token.json()["data"]["ticket"]
cookie = token.json()["data"]["CSRFPreventionToken"]
s.headers = {"Cookie": f"PVEAuthCookie={ticket}", "CSRFPreventionToken": f"{cookie}"}
cluster_res = s.get(url + "/api2/json/cluster/resources")

inventory = {}
for res in cluster_res.json()['data']:
    if res['type'] != 'qemu':
        continue
    config = s.get(url + "/api2/json/nodes/{}/qemu/{}/config".format(res["node"], res["vmid"])).json()
    ipconfig = config["data"].get("ipconfig0")
    if ipconfig:
        ip_address = re.search(r'ip=([0-9.]+)/\d+', ipconfig).groups()[0]
        if ip_address:
            inventory['qemu_{}'.format(res['vmid'])] = {"hosts": [ip_address,], "vars": {"name": res["name"], "node": res["node"]}}

print(json.dumps(inventory, indent=2))
