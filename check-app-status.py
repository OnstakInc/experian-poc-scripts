#!/usr/bin/python3 -u
import time
import argparse
from modules import morpheus_apis

#########################################################
# Command Line Arguments ################################
#########################################################
parser = argparse.ArgumentParser()
parser.add_argument('--name', type=str, help='Stack Name', required=True)
args = parser.parse_known_args()[0]
#########################################################


#########################################################
# Check Stack Status ####################################
#########################################################
print('INFO: Checking Statck Status...')

app = next(filter(lambda e: e.get('name').upper() == args.name.upper(), morpheus_apis.get_apps().get('apps')), None)

if not app:
    print(f'ERROR: Stack {args.name} does not exist.')
    exit(1)


while True:
    result = morpheus_apis.get_apps(app.get('id'))

    print(result.get('app'))

    print(f"INFO: Stack Status: {result.get('app').get('appStatus')}")

    if result.get('app').get('appStatus') == 'failed':
        print(f"ERROR: Stack Provisioning Failed: {args.name}")
        exit(1)

    if result.get('app').get('appStatus') == 'completed':
        print(f"INFO: Stack Provisioned: {args.name}")
        exit()

    time.sleep(15)
#########################################################