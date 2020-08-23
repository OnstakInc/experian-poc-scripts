import os
import sys
import json
import requests
import argparse

#########################################################
# Environment Variables #################################
#########################################################
USERNAME = os.environ.get('USERNAME')
PASSWORD = os.environ.get('PASSWORD')
MORPHEUS_URL = os.environ.get('MORPHEUS_URL')
#########################################################


#########################################################
# API Methods ###########################################
#########################################################
def get_auth_token():

    url = f'{MORPHEUS_URL}/oauth/token?grant_type=password&scope=write&client_id=morph-api'

    payload = {
        'username': USERNAME,
        'password': PASSWORD
    }

    result = requests.post(url, data=payload, verify=False)

    return json.loads(result.content)['access_token']

def get_apps(app_id=None):
    
    url = f'{MORPHEUS_URL}/api/apps/{app_id}' if app_id else  f'{MORPHEUS_URL}/api/apps'

    headers = {
        'Authorization': f'Bearer {get_auth_token()}'
    }

    result = requests.get(url, headers=headers, verify=False)

    return json.loads(result.content)

def create_apps(data):
    
    url = f'{MORPHEUS_URL}/api/apps'

    headers = {
        'Authorization': f'Bearer {get_auth_token()}'
    }

    result = requests.post(url, headers=headers, data=json.dumps(data), verify=False)

    return json.loads(result.content)

def get_blueprints(blueprint_id=None):
    
    url = f'{MORPHEUS_URL}/api/blueprints/{blueprint_id}' if blueprint_id else f'{MORPHEUS_URL}/api/blueprints'

    headers = {
        'Authorization': f'Bearer {get_auth_token()}'
    }

    result = requests.get(url, headers=headers, verify=False)

    return json.loads(result.content)
#########################################################