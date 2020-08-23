#!/usr/bin/python3 -u
import json
import argparse
from modules import morpheus_apis

#########################################################
# Command Line Arguments ################################
#########################################################
parser = argparse.ArgumentParser()

parser.add_argument('--name', type=str, help='Stack Name', required=True)
parser.add_argument('--cloud', type=str, help='Cloud Name', required=True)
parser.add_argument('--blueprint', type=str, help='JSON Blueprint Path', required=True)

args = parser.parse_known_args()[0]
#########################################################


#########################################################
# Validate Stack Name ###################################
#########################################################
result = next(filter(lambda e: e.get('name').upper() == args.name.upper(), morpheus_apis.get_apps().get('apps')), None)

if result:
    print(f'ERROR: Stack already exists with name {args.name}.')
    exit(1)

print(f'INFO: Stack Name Validated: {args.name}.')
#########################################################


#########################################################
# Provision App #########################################
#########################################################
blueprint = json.loads(open(args.blueprint, 'r').read())

blueprint['name'] = args.name

app = morpheus_apis.create_apps(blueprint)

print(f'INFO: Stack Provisioning: {args.name}')
#########################################################