import os
import json
import argparse
from modules import morpheus_apis
from tetpyclient import RestClient

#########################################################
# Global Variables ######################################
#########################################################
TETRATION_URL = os.environ.get('TETRATION_URL')
TETRATION_API_KEY = os.environ.get('TETRATION_API_KEY')
TETRATION_API_SECRET = os.environ.get('TETRATION_API_SECRET')

MORPHEUS_SCOPE_ID = '5f43ca61497d4f096c203ee6'
#########################################################


#########################################################
# Command Line Arguments ################################
#########################################################
parser = argparse.ArgumentParser()

parser.add_argument('--name', type=str, help='Stack Name', required=True)

args = parser.parse_known_args()[0]
#########################################################


#########################################################
# Get App Tiers Info ####################################
#########################################################
result = next(filter(lambda e: e.get('name').upper() == args.name.upper(), morpheus_apis.get_apps().get('apps')), None)

if not result:
    print(f'WARNING: Stack Does Not Exist: {args.name}')
    exit()

app_tiers = []

for app_tier in result.get('appTiers'):

    name = app_tier.get('tier').get('name')

    evars = list(map(lambda e: e.get('instance').get('evars'), app_tier.get('appInstances')))

    for item in evars:

        filter_ips = list(filter(lambda e: 'CENTOS_IP' in e.get('name'), item))

        ips = list(map(lambda e: e.get('value'), filter_ips))

        app_tiers.append({
            'name': name,
            'instances': ips
        })

print(f'INFO: App Tiers: {json.dumps(app_tiers)}')
#########################################################


#########################################################
# Create Tetration REST Client ##########################
#########################################################
tet_client = RestClient(
    server_endpoint=TETRATION_URL,
    api_key=TETRATION_API_KEY,
    api_secret=TETRATION_API_SECRET,
    verify=True
)
#########################################################


#########################################################
# Create Tetration Scopes ###############################
#########################################################
req_number = args.name.split('-')[-1]

print(f'INFO: Ticket Number: {req_number}')

print('INFO: Creating Tetration Scopes')

for app_tier in app_tiers:

    filters = list(map(lambda e: { 
        'type': 'eq',
        'field': 'ip',
        'value': e
    }, app_tier.get('instances')))

    req_payload = {
        'short_name': f"{app_tier.get('name')}_{req_number}",
        'description': 'Provisioned By Morpheus',
        'short_query': {
            'type': 'or',
            'filters': filters
        },
        'parent_app_scope_id': MORPHEUS_SCOPE_ID
    }

    resp = tet_client.post('/app_scopes', json_body=json.dumps(req_payload))

    # print(f"INFO: Tetration Scope Created: {resp.text}")
    print(f"INFO: Tetration Scope Created: {app_tier.get('name')}_{req_number}")
#########################################################


#########################################################
# Create Tetration Apps #################################
#########################################################
print('INFO: Creating Tetration Applications')

for app_tier in app_tiers:

    scopes = json.loads(tet_client.get('/openapi/v1/app_scopes/').text)

    for scope in scopes:

        full_name = f"ONSTAK:Morpheus:{app_tier.get('name')}_{req_number}"

        if scope['name'] == full_name:

            application = {
                'app_scope_id': scope['id'],
                'name': app_tier.get('name'),
            }

            resp = tet_client.post('/applications', json_body=json.dumps(application))

            print(f"INFO: Tetration App Created: {app_tier.get('name')}_{req_number}")
#########################################################
print('INFO: Tasks Completed Successfully.')
