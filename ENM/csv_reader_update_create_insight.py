import csv
import requests
from dotenv import dotenv_values
from insight_attributes_map import attributes_map
import json
# import os

config = dotenv_values("../.env")
headers = {'Content-Type': 'application/json'}


def update_insight_object(data, obj_id):
    fields = {"objectTypeId": config.get('type_id'), "attributes": []}

    for key, value in data.items():
        fields["attributes"].append(
            {
                "objectTypeAttributeId": attributes_map[key],
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
    fields = {"objectTypeId": config.get('type_id'), "attributes": []}

    for key, value in data.items():
        fields["attributes"].append(
            {
                "objectTypeAttributeId": attributes_map[key],
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
    serial_number = data.get('Serial Number')
    inventory_unit = data.get('Inventory Unit')
    params = {
        "objectSchemaId": 1,
        "iql": f'ObjectTypeId={config.get("type_id")} AND "Serial Number" = "{serial_number}" AND "Inventory Unit" = "{inventory_unit}"',
        "resultPerPage": 5
    }
    insight_iql_link = f'http://[JIRA IP]/rest/insight/1.0/iql/objects?'
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
        print(f"******** {serial_number} and {inventory_unit} has multiple record ********")
        raise Exception


def reader(file):
    with open(file, newline='') as csvfile:
        print(f"Openning file {file} <-----")
        csv_reader = csv.DictReader(csvfile)
        for row in csv_reader:
            print(f"Inserting Row with Data ====>>>>{row['Serial Number']}, ^^^^^^^, {row['Inventory Unit']}")
            try:
                result = search_in_insight(row)
            except:
                continue
            if result != 'create':
                update_insight_object(row, result)
            else:
                create_insight_object(row)
