#!/bin/python
# -*- coding: utf-8 -*-

import sys
import requests
import json
import urllib3
import base64
import getpass

esmuser = input("Username: ");
esmpass = getpass.getpass(prompt="Password: ");
esmip = input("ESM IP: ");

# Config options: URL to connect to, send calls to, and user/pass
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

# The API call that we're making
# call = input("API Call > ")
call = 'qryExecuteDetail?type=EVENT&reverse=false'

# Login and get the token
r1 = client.post(authUrl, verify=False, json=authBody)

token = r1.headers['Xsrf-Token']

headers = { "X-XSRF-TOKEN": token }

fh = open("./apicall.json", "r")
data = fh.read()

# Make the call
r2 = client.post(url+call, headers=headers, data=data)

print (r2.text)
parsedJson2 = r2.json()
resultID2 = parsedJson2['resultID']
print (resultID2);

getres = 'qryGetResults?startPos=0&numRows=10&reverse=false'
data3 = { "resultID": resultID2 }

r3 = client.post(url+getres, headers=headers, json=data3)
print(r3.text)

close = 'qryClose?resultID='+resultID2
r3 = client.post(url+close, headers=headers)

print ("\n\n*** Random debug stuff ***")
print("URL:", url+call)
print("URL2:", url+getres)
print('Result ID from r2:', resultID2)
print("Status1:", r1.status_code)
print("Status2:", r2.status_code)
print("Status3:", r3.status_code)
