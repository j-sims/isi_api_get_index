#!/usr/bin/env python3
import requests
import json
import os
from requests.exceptions import RequestException

# Suppress insecure HTTPS request warnings for self-signed certificates
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

# Configuration settings potentially from environment variables
CLUSTER_IP = os.getenv('CLUSTER_IP')
PORT = os.getenv('PORT')
USER = os.getenv('USER')
PASSWORD = os.getenv('PASSWORD')

# API endpoint construction
BASE_URL = f"https://{CLUSTER_IP}:{PORT}"
AUTH_URL = f"{BASE_URL}/session/1/session"
API_URL = f"{BASE_URL}/platform"

# Headers for sending/receiving JSON
HEADERS = {'Content-Type': 'application/json'}

# Start session to manage cookies and headers
session = requests.Session()

def authenticate():
    """Authenticate with the cluster and setup CSRF protection."""
    auth_data = json.dumps({'username': USER, 'password': PASSWORD, 'services': ['platform']})
    try:
        response = session.post(AUTH_URL, data=auth_data, headers=HEADERS, verify=False)
        response.raise_for_status()
        
        # Set headers for CSRF protection
        session.headers['referer'] = BASE_URL
        session.headers['X-CSRF-Token'] = session.cookies.get('isicsrf')
        return True
    except RequestException as e:
        print(f"Authorization Failed: {str(e)}")
        print(f"Response Status Code: {response.status_code}")
        print(f"Response Text: {response.text}")
        return False

def fetch_lins(index_name="cluster_lin_index"):
    """Fetch Logical Interface Numbers (LINs) from the cluster API."""
    lins = []
    endpoint = f'/8/fsa/index/{index_name}/lins'
    try:
        response = session.get(f"{API_URL}{endpoint}", verify=False)
        response.raise_for_status()
        result = response.json()
        lins.extend(result['lins'])

        while result.get('resume'):
            endpoint += f"?resume={result['resume']}"
            response = session.get(f"{API_URL}{endpoint}", verify=False)
            response.raise_for_status()
            result = response.json()
            lins.extend(result['lins'])

    except RequestException as e:
        print(f"Failed to fetch LINs: {str(e)}")
    return lins

def main():
    if authenticate():
        lins = fetch_lins()
        print(f"There are {len(lins)} files")
        if lins:
            print(lins[0])

if __name__ == "__main__":
    main()
