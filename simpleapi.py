#!/bin/python

import sys
import requests
import json
import urllib3

esmuser = input("Username: ")
esmpass = getpass.getpass(prompt="Password: ")
esmip = input("ESM IP: ")

# Config options: URL to connect to, send calls to, and user/pass.
authUrl = "https://{}/rs/esm/login/".format(esmip);
url = "https://{}/rs/esm/v2/".format(esmip);

esmuser = base64.b64encode(esmuser.encode('utf-8'));
esmuser = esmuser.decode('utf-8')
esmpass = base64.b64encode(esmpass.encode('utf-8'));
esmpass = esmpass.decode('utf-8')

authBody = { "username": "{}".format(esmuser), "password": "{}".format(esmpass), "locale": "en_US" }

# Silence the annoying insecure warning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Start a session
client = requests.session()

# Login and get the token
r1 = client.post(authUrl, verify=False, json=authBody)

token = r1.headers['Xsrf-Token']

headers = { "X-XSRF-TOKEN": token }

# The API call that we're making
# call = input("API Call > ")
call = 'qryGetSelectFields'
#data = {"resultID": {'3533729092'}}

# Make the call
r2 = client.post(url+call, headers=headers, json=data)
print(r2.text)

print ("\n\n*** Random debug stuff ***")
print("URL: ")
print(url+call)
print("\nStatus: ")
print(r2.status_code)
