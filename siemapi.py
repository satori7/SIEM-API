#!/bin/python
# -*- coding: utf-8 -*-

import os
import re
import sys
import time
import json
import base64
import getpass
import logging
import urllib3
import requests
import argparse
import threading
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

# Get arguments. Put filename into args.input. Make help text.
parser = argparse.ArgumentParser(description='Retrieve events from the McAfee ESM.')
parser.add_argument('--input', '-i', type=str, help='Filename of API Query')
args = parser.parse_args()

# Set up logging.
logging.basicConfig(filename='./debug.log',
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)-8s %(message)s',
    datefmt='%m-%d-%y %H:%M:%S')

logging.info("SIEM-API started.")

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

# Silence the annoying insecure warning.
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Start a session and keep it from being a jerk.
client = requests.session()
retry = Retry(connect=3, backoff_factor=0.5)
adapter = HTTPAdapter(max_retries=retry)
client.mount('http://', adapter)
client.mount('https://', adapter)

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

print("Authenticated.")

# Create a keep alive.
def keepAlive(t):
    while True:
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        time.sleep(1) # Need to pause to prevent oversubscription?
        call = "miscKeepAlive"
        ka = client.post(url+call, verify=False, headers=headers)
        time.sleep(t)
        print(".")
        global tstop
        if tstop:
            break

# Start the keep alive thread.
tstop = False
thread = threading.Thread(target=keepAlive, args=(5, ))
thread.start()

# The API call that we're making.
call = 'qryExecuteDetail?type=EVENT&reverse=false'

# Read the JSON from file.
if args.input:
    ifile = args.input
    fh = open(ifile, "r")
else:
    fh = open('apicall.json', 'r')
data = fh.read()

# Make the call.
r2 = client.post(url+call, headers=headers, data=data)
parsedJson2 = r2.json()
resultID2 = parsedJson2['resultID']

# Check to see if the job is done.
statusCall = "qryGetStatus"
data4 = { "resultID": { "{}".format(resultID2) }}
while True:
    try:
        r4 = client.post(url+statusCall, headers=headers, params=data4)
    except requests.exceptions.RequestException as e:
        print(e)
        sys.exit(1)
    print('Query Percent Complete:')
    print(r4.json()['percentComplete'])
    time.sleep(2)
    completion = r4.json()['complete']
    if completion == True:
        break

# Now that the query is done, get the results.
timestart = time.time()
fw = open("output.json","w+")
print("Getting results...")
rows = 0
while True:
    getres = 'qryGetResults?startPos={}&numRows=1000000&reverse=false'.format(rows)
    data3 = { "resultID": resultID2 }
    try:
        r3 = client.post(url+getres, headers=headers, json=data3)
    except requests.exceptions.RequestException as e:
        logging.CRITICAL(e)
        print(e)
        sys.exit(1)
    rows = rows + 10000
    # Write the results to a file
    fw.write(r3.text)
    print("Running for %s seconds." % (round(time.time() - timestart)))
    #TODO: This is really hacky. Find a better way of doig this (once I have another SIEM to work with).
#    fsize = os.stat('./output.json')
#    lastrow = str(r3.json()['columns'])
#    if fsize.st_size > 10000 and re.search('name', lastrow):
#        break

# Close the result so the ESM doesn't get jammed up
close = 'qryClose?resultID='+resultID2
try:
    r3 = client.post(url+close, headers=headers)
except requests.exceptions.RequestException as e:
    logging.CRITICAL(e)
    print(e)
    sys.exit(1)
logging.info("Result closed.")

# Stop the keepAlive thread
tstop = True
thread.join()
logging.info("Keep alive thread closed")

logging.info("Complete")
print("Complete")
