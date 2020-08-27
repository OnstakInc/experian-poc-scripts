import os
import sys
import json
import base64
import requests
import argparse

requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

#########################################################
# Environment Variables #################################
#########################################################
SNOW_USERNAME = os.environ.get('SNOW_USERNAME')
SNOW_PASSWORD = os.environ.get('SNOW_PASSWORD')
SNOW_URL = os.environ.get('SNOW_URL')
#########################################################


#########################################################
# API Methods ###########################################
#########################################################
def basic_auth():
    return base64.b64encode(f'{SNOW_USERNAME}:{SNOW_PASSWORD}'.encode('utf-8')).decode('utf-8')


def get_sc_req_item_by_number(number):

    url = f'{SNOW_URL}/api/now/table/sc_req_item?number={number}'

    headers = {
        'Authorization': f'Basic {basic_auth()}'
    }

    result = requests.get(url, headers=headers, verify=False)

    return json.loads(result.content)


def update_sc_req_item(req_id, data):

    url = f'{SNOW_URL}/api/now/table/sc_req_item/{req_id}'

    headers = {
        'Authorization': f'Basic {basic_auth()}'
    }

    result = requests.put(url, headers=headers, data=json.dumps(data), verify=False)

    return json.loads(result.content)
#########################################################