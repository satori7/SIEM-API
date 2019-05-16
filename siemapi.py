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

# Config options: URL to connect to, send calls to, and user/pass.
authUrl = "https://{}/rs/esm/login/".format(esmip);
url = "https://{}/rs/esm/v2/".format(esmip);

esmuser = base64.b64encode(esmuser.encode('utf-8'));
esmuser = esmuser.decode('utf-8')
esmpass = base64.b64encode(esmpass.encode('utf-8'));
esmpass = esmpass.decode('utf-8')
authBody = { "username": "{}".format(esmuser), "password": "{}".format(esmpass), "locale": "en_US" }

# Silence the annoying insecure warning.
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Start a session.
client = requests.session()

# Login and get the token.
try:
    r1 = client.post(authUrl, verify=False, json=authBody)
except requests.exceptions.RequestException as e:
    print(e)
    sys.exit(1)

try:
    token = r1.headers['Xsrf-Token']
except:
    print("\nFailed to authenticate.\n")
    sys.exit(1)

headers = { "X-XSRF-TOKEN": token }

dsid = input("Authenticated. Please enter the data source ID: ")

# The API call that we're making.
call = 'qryExecuteDetail?type=EVENT&reverse=false'

# Read the JSON from file.
fh = open("./apicall.json", "r")
data = fh.read().replace('$DSID', dsid)

# Make the call.
r2 = client.post(url+call, headers=headers, data=data)
parsedJson2 = r2.json()
resultID2 = parsedJson2['resultID']

# Check to see if the job is done.
statusCall = "qryGetStatus"
data4 = { "resultID": { "{}".format(resultID2) }}
try:
    r4 = client.post(url+statusCall, headers=headers, params=data4)
except requests.exceptions.RequestException as e:
    print(e)
    sys.exit(1)
parsedJson4 = r4.json()
while parsedJson4['complete'] == "False":
    print("Still cookin'\n")
    sleep(1)

# Now that the query is done, get the results.
getres = 'qryGetResults?startPos=0&numRows=5000000&reverse=false'
data3 = { "resultID": resultID2 }
try:
    r3 = client.post(url+getres, headers=headers, json=data3)
except requests.exceptions.RequestException as e:
    print(e)
    sys.exit(1)

# Write the results to a file
fw = open("output.json","w+")
fw.write(r3.text)

# Close the result so the ESM doesn't get jammed up
close = 'qryClose?resultID='+resultID2
r3 = client.post(url+close, headers=headers)

########################################
# Debugging
print ("\n\n*** Random debug stuff ***")
print("URL:", url+call)
print("URL2:", url+getres)
print('Result ID from r2:', resultID2)
print("Status1:", r1.status_code)
print("Status2:", r2.status_code)
print("Status3:", r3.status_code)
print("Status4:", r4.status_code)
print("r4 Message: ", r4.text)
