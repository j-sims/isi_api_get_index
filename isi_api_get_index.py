#!/usr/bin/env python3
import requests
import json
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) # Supresses the self signed cert warning

CLUSTERIP = '172.16.10.10'
PORT=8080
USER='root'
PASS='a'

# uri of the cluster used in the referer header
uri = f"https://{CLUSTERIP}:{PORT}"
# url of Papi used for all further calls to Papi
papi = uri + '/platform'
# Set header as content will provided in json format
headers = {'Content-Type': 'application/json'}
# Create json dictionary for auth
data = json.dumps({'username': USER, 'password': PASS, 'services': ['platform']})
# create a session object to hold cookies
session = requests.Session()
# Establish session using auth credentials
response = session.post(uri + "/session/1/session", data=data, headers=headers, verify=False)
if 200 <= response.status_code < 299:
    # Set headers for CSRF protection. Without these two headers all further calls with be "auth denied"
    session.headers['referer'] = uri
    session.headers['X-CSRF-Token'] = session.cookies.get('isicsrf')
else:
    print("Authorization Failed")
    print(response.content)

lins = []
indexname = "cluster_lin_index"
endpoint = '/8/fsa/index/cluster_lin_index/lins'

response = session.get(papi + endpoint, verify=False)
result = json.loads(response.content)
lins += result['lins']

if result['resume']:
    key=result['resume']
    while result['resume']:

        endpoint = f'/8/fsa/index/cluster_lin_index/lins?resume={key}'
        response = session.get(papi + endpoint, verify=False)
        result = json.loads(response.content)
        key=result['resume']
        lins += result['lins']

print(f"There are {len(lins)} files")
print(lins[0])

