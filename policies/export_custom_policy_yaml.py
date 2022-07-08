import json
import os
import sys

import requests
import yaml


def run():
    bc_api_url = os.environ.get(
        'BC_API_URL', 'https://www.bridgecrew.cloud/api/v1')
    api_key = os.environ.get('BC_API_KEY')
    policy_endpoint = '/policies/table/data'
    if not api_key:
        print("Please set the API key as an environment variable: BC_API_KEY")
        sys.exit(1)
    headers = {"Accept": "application/json", "Authorization": f"{api_key}"} 
    policy_data = requests.get(
        url=f"{bc_api_url}{policy_endpoint}", headers=headers)
    policy_data_dict = json.loads(policy_data.text)
    for p in policy_data_dict['data']:
        if p.get('isCustom'):
            code = p.get('code')
            if not code:
                print(f"{p.get('id')}: {p.get('title')} --> is a visual editor policy")
                continue
            yaml_code = yaml.safe_load(code)
            severity = yaml_code['metadata']['severity']
            if severity.lower() == 'critical':
                print(f"changing critical severity to high for {p.get('id')}")
                yaml_code['metadata']['severity'] = "high"
            print(f"writing: {p.get('id')}")
            with open(f"{p.get('id')}.yaml", '+w') as f:
                f.write(yaml.dump(yaml_code, sort_keys=False))
                f.close()


if __name__ == '__main__':
    run()
