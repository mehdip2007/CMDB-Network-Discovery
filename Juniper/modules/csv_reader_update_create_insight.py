import json
import requests
from dotenv import dotenv_values
from .juniper_insight import juniper_insight_attribute_ids
config = dotenv_values("../env")
headers = {'Content-Type': 'application/json'}


def update_insight_object(data, obj_id):
    fields = {"objectTypeId": config.get('juniper_type_id'), "attributes": []}

    for key, value in data.items():
        fields["attributes"].append(
            {
                "objectTypeAttributeId": juniper_insight_attribute_ids[key],
                "objectAttributeValues": [{"value": value if value is not None else "-"}],
            }
        )

    try:
        response = requests.put(
            'http://[JIRA IP]/rest/insight/1.0/' + f"object/{obj_id}/",
            auth=(config.get("insight_username"), config.get("insight_password")),
            data=json.dumps(fields),
            headers=headers,
            verify=False,
        )
        print(response)
    except Exception as e:
        print(e, "******")
        return

    if response.status_code != 201:
        print(f"{response.status_code} for {data.get('Serial Numbers')}")



def create_insight_object(data):
    fields = {"objectTypeId": config.get('juniper_type_id'), "attributes": []}

    for key, value in data.items():
        fields["attributes"].append(
            {
                "objectTypeAttributeId": juniper_insight_attribute_ids[key],
                "objectAttributeValues": [{"value": value}],
            }
        )
    print(json.dumps(fields))
    try:
        response = requests.post(
            'http://[JIRA IP]/rest/insight/1.0/' + "object/create/",
            auth=(config.get("insight_username"), config.get("insight_password")),
            data=json.dumps(fields),
            headers=headers,
            verify=False,
        )
        print(response.url)
    except Exception as e:
        print(e, "******")
        return

    if response.status_code != 201:
        print(f"{response.status_code} for {data.get('Serial Numbers')}")
        print(response.text)


def search_in_insight(data):
    ip_address = data.get('ip_address')
    device_model = data.get('device_model')
    params = {
        "objectSchemaId": 1,
        "iql": f'ObjectTypeId={config.get("juniper_type_id")} AND ""IP Address" = "{ip_address}" AND "Device Model" = "{device_model}"',
        "resultPerPage": 5
    }
    insight_iql_link = 'http://[JIRA IP]/rest/insight/1.0/iql/objects?'
    responses = requests.get(insight_iql_link,
                             auth=(config.get("insight_username"), config.get("insight_password")), verify=False,
                             params=params)
    json_response = responses.json()

    if len(json_response['objectEntries']) == 1:
        print("In Len 1 ---> ")
        return json_response['objectEntries'][0]["id"]
    if len(json_response['objectEntries']) == 0:
        print("In Len 0 ---> ")
        return 'create'
    else:
        print("In Exception ---> ")
        print(len(json_response['objectEntries']))
        print(f"******** {ip_address} and {device_model} has multiple record ********")
        raise Exception
