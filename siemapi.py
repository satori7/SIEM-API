#!/bin/python

import sys
import requests
import json
import urllib3

# Config options: URL to connect to, send calls to, and user/pass
authUrl = 'https://10.57.12.95/rs/esm/login/'
url = 'https://10.57.12.95/rs/esm/v2/'
# Uncomment for apiuser
# authBody = { "username": "YXBpdXNlcgo=", "password": "U2VjdXJpdHkuNHU=", "locale": "en_US" }
# Uncomment for NGCP
authBody = { "username": "TkdDUA==", "password": "U2VjdXJpdHkuNHU=", "locale": "en_US" }

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
# parsedJson2 = r2.json()
# resultID2 = parsedJson2['resultID']

close = 'qryClose?resultID='+resultID2

r3 = client.post(url+close, headers=headers)

#parsedJson3 = r3.json()
#resultID3 = parsedJson3['resultID']

getres = 'qryGetResults?startPos=0&numRows=0&reverse=false'
data3 = { "resultID": resultID2 }

r4 = client.post(url+getres, headers=headers, json=data3)
print(r4.text)

print ("\n\n*** Random debug stuff ***")
print("URL:", url+call)
print("URL2:", url+getres)
print('Result ID from r2:', resultID2)
#print('Result ID from r3:', resultID3)
print("Status1:", r1.status_code)
print("Status2:", r2.status_code)
print("Status3:", r3.status_code)
print("Status4:", r4.status_code)
