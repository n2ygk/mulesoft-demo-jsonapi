#!/usr/bin/env python3
"""
Make some clean test data
"""
import json
import sys
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

token=sys.argv[1]
objs = 'https://127.0.0.1:8082/v1/api/objects'
locs = 'https://127.0.0.1:8082/v1/api/locations'
wids = 'https://127.0.0.1:8082/v1/api/widgets'

headers = {
    'authorization': 'Bearer ' + token,
    'content-type': "application/vnd.api+json",
}

locations = [
    {
        "type": "locations",
        "attributes": {
            "warehouse": "Secaucus",
            "aisle": "1",
            "shelf": "2",
            "bin": "3"
        }
    },
    {
        "type": "locations",
        "attributes": {
            "warehouse": "NYC",
            "aisle": "11",
            "shelf": "22",
            "bin": "33"
        }
    },
    {
        "type": "locations",
        "attributes": {
            "warehouse": "Briarcliff Manor",
            "aisle": "4",
            "shelf": "5",
            "bin": "6"
        }
    },
]

locIds = []


response = requests.request("DELETE", objs, headers=headers, verify=False)
print(response)

for l in locations:
    payload = { "data": l }
    response = requests.request("POST", locs, data=json.dumps(payload), headers=headers,verify=False)
    if response.status_code < 400:
        r = json.loads(response.text)
        locIds.append(r['data']['id'])
    else:
        print(response.text)
        exit(1)

print(locIds)

widgets = [
    {
        "type": "widgets",
        "attributes": {
            "name": "can opener",
            "qty": 123
        },
        "relationships": {
            "locations": [
                {
                    "type": "locations",
                    "id": locIds[0]
                },
                {
                    "type": "locations",
                    "id": locIds[1]
                },
            ],
            "manufacturer": {
                "type": "companies",
                "id": "none"
            }
        }
    },
    {
        "type": "widgets",
        "attributes": {
            "name": "church key",
            "qty": 1
        }
    },
    {
        "type": "widgets",
        "attributes": {
            "name": "stapler",
        },
        "relationships": {
            "locations": [
                {
                    "type": "locations",
                    "id": locIds[2]
                },
            ]
        }
    },
]

widIds = []
for w in widgets:
    payload = { "data": w }
    response = requests.request("POST", wids, data=json.dumps(payload), headers=headers,verify=False)
    if response.status_code < 400:
        r = json.loads(response.text)
        widIds.append(r['data']['id'])
    else:
        print(response.text)
        exit(1)

print(widIds)
