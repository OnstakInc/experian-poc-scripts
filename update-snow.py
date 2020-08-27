#!/usr/bin/python3 -u
import argparse
from modules import snow_apis

#########################################################
# Command Line Arguments ################################
#########################################################
parser = argparse.ArgumentParser()

parser.add_argument('--name', type=str, help='Stack Name', required=True)

args = parser.parse_known_args()[0]
#########################################################


#########################################################
# Update SNOW Ticket Status #############################
#########################################################
req_number = args.name.split('-')[-1]

print(f'INFO: Ticket Number: {req_number}')

item = snow_apis.get_sc_req_item_by_number(req_number)

if len(item.get('result')) > 0:

    print(f'INFO: Ticket ID: {item.get("result")[0].get("sys_id")}')

    data = {
        'state': '3',
        'comments': 'Stack provisioning complete.'
    }

    result = snow_apis.update_sc_req_item(req_id=item.get('result')[0].get('sys_id'), data=data)

    print(f'INFO: Updated SNOW Ticket: {req_number}')

#########################################################