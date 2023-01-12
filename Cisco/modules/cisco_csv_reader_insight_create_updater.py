import csv
import os
import requests
from dotenv import dotenv_values
from .cisco_insight_attributes_map import attributes_map
import json


config = dotenv_values("../.env")
headers = {'Content-Type': 'application/json'}


def update_insight_object(data, obj_id):
    fields = {"objectTypeId": config.get('cisco_type_id'), "attributes": []}

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
    """
        since JIRA uses specific type of json first we need to create it with combination of our csv file and attributes
        map python file with iteration.
    """

    fields = {"objectTypeId": config.get('cisco_type_id'), "attributes": []}

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
        print(response.status_code)
    except Exception as e:
        print(e, "******")
        return


def search_in_insight(data):
    """
        get the serial_number mad and cisco_ios_software version to make our IQL query for insight which used in params
    """
    serial_number = data.get('Serial Number')
    cisco_ios_software = data.get('CISCO IOS Software')
    params = {
        "objectSchemaId": 1,
        "iql": f'ObjectTypeId={config.get("cisco_type_id")} AND "Serial Number" = "{serial_number}" AND "CISCO IOS Software" = "{cisco_ios_software}"',
        "resultPerPage": 5
    }
    insight_iql_link = f'http://[JIRA IP]/rest/insight/1.0/iql/objects?'
    responses = requests.get(insight_iql_link,
                             auth=(config.get("insight_username"), config.get("insight_password")), verify=False,
                             params=params)
    json_response = responses.json()

    """
        if data was found per csv row we call the update method based on IQL update method is called
        if data wast not found (0) per csv row we call the create method based on IQL update method is called
        else error is return.
    """

    if len(json_response['objectEntries']) == 1:
        print("In Len 1 ---> ")
        return json_response['objectEntries'][0]["id"]
    if len(json_response['objectEntries']) == 0:
        print("In Len 0 ---> ")
        return 'create'
    else:
        print("In Exception ---> ")
        print(len(json_response['objectEntries']))
        print(f"******** {serial_number} and {cisco_ios_software} has multiple record ********")
        raise Exception


"""
    read our csv file file to find the data and check whether out data exists on NWG Insight or not     
"""


def reader(file):
    print(" ************* File Found.")
    print(file)
    if os.path.isfile(file):
        with open(file, newline='') as csvfile:
            print(f"Openning file {file} <-----")
            csv_reader = csv.DictReader(csvfile)
            for row in csv_reader:
                print(f"Inserting Row with Data ====>>>> {row['Name']}, ^^^^^^^, {row['IP Address']}")
                try:
                    result = search_in_insight(row)
                except:
                    continue
                if result != 'create':
                    update_insight_object(row, result)
                else:
                    create_insight_object(row)
