#!/bin/python

import sys
import requests
import json
import urllib3

# Config options: URL to connect to, send calls to, and user/pass
authUrl = 'https://10.57.12.242/rs/esm/v2/login/'
url = 'https://10.57.12.242/rs/esm/v2/'
authBody = { "username": "TkdDUA==", "password": "U2VjdXJpdHkuNHU=", "locale": "en_US" }
# authBody = { "username": "YXBpdXNlcgo=", "password": "U2VjdXJpdHkuNHU=", "locale": "en_US" }

# Silence the annoying insecure warning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Start a session
client = requests.session()

# The API call that we're making
# call = input("API Call > ")
call = 'qryGetStatus'
data = '{"resultID": {"value": 4485633587}}'

# Login and get the token
r1 = client.post(authUrl, verify=False, json=authBody)

token = r1.headers['Xsrf-Token']

headers = { "X-XSRF-TOKEN": token }

# Make the call
r2 = client.post(url+call, headers=headers, data=data)

print(r2.text)

print ("\n\n*** Random debug stuff ***")
print("URL: ")
print(url+call)
print("\nStatus: ")
print(r2.status_code)
