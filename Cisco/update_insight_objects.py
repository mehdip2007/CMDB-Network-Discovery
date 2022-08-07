import pandas as pd
import numpy as np
import requests
import json
from pprint import pprint


class NetworkInsightCreateUpdate:
    def __init__(self, insight_username, insight_password):
        self.insight_username = insight_username
        self.insight_password = insight_password
        self.insight_object_name = ""
        self.all_insights_object_entries = []
        self.object_type_attributes = []
        self.object_attributes_id_name = {}
        self.data = {}

    def get_object_entires(self, insight_object_name):
        link = "http://10.132.58.167/rest/insight/1.0/objectschema/1/objecttypes/flat"

        try:
            responses = requests.get(link, auth=(self.insight_username, self.insight_password), verify=False)
            print("Getting NWG Objects...")
            print("Status --> ", responses.status_code)
            for response in responses.json():
                if response['name'] == insight_object_name:
                    print(f"Object {response['name']} ID is {response['id']}")
                    self.insight_object_name = response['name']

                    _id = response['id']
                    self.data["objectTypeId"] = _id

            # pprint(self.data)
                    self.get_object_entries(response)
            return True
        except Exception as err:
            print(err, '&&&&&&&')
            return False

    def get_object_entries(self, response):
        link = f"http://10.132.58.167/rest/insight/1.0/iql/objects?\
                          objectSchemaId={response.get('objectSchemaId')}&iql=ObjectTypeId=\
                         {self.data.get('objectTypeId')}&resultPerPage=500000"

        try:
            responses = requests.get(link, auth=(self.insight_username, self.insight_password), verify=False)
            print(f"Getting Object {self.insight_object_name} Attributes --->")
            response = responses.json()

            all_insights_object_entries = response['objectEntries']
            object_type_attributes = response['objectTypeAttributes']

            for object_entries in all_insights_object_entries:
                # print(object_entries['objectKey'])
                self.all_insights_object_entries.append({object_entries['name']: object_entries['objectKey']})

            for type_attributes in object_type_attributes:
                attribute_name = type_attributes['name']
                attribute_id = type_attributes['id']

                self.object_attributes_id_name.update({attribute_name: attribute_id})

            return True
        except Exception as e:
            print(e, '******')

    def update_or_create_insight(self, data):
        df = pd.read_csv(data)
        df = df.replace({np.nan: "-"})
        df.rename(columns={'Hostname': 'Name'}, inplace=True)

        attributes = {}
        data_list = []
        for index, row in df.iterrows():
            attributes_list = []
            for attribute_name, attribute_id in self.object_attributes_id_name.items():
                if attribute_name not in ("Key", "Created", "Updated", "Device Modules", "IP Address"):
                    attributes['objectTypeAttributeId'] = attribute_id
                    attributes['objectAttributeValues'] = []
                    attributes['objectAttributeValues'].append({'value': row[attribute_name]})

                    # print(attributes)
                    attributes_copy = attributes.copy()
                    attributes_list.append(attributes_copy)

            data_copy = self.data.copy()
            data_copy.update({'attributes': attributes_list})
            data_list.append(data_copy)

        for data in data_list:
            flag = True
            for items in self.all_insights_object_entries:
                data_hostname = data['attributes'][0]['objectAttributeValues'][0]['value']
                if data_hostname == list(items)[0]:
                    flag = False
                    print(f"{list(items)[0]} equal to === {data_hostname}")
                    print(f"Updating Data for {list(items)[0]}...")
                    object_key = items[list(items)[0]]
                    self.update_nwg_insight(data, object_key)

            if flag:
                self.create_nwg_insight(data)

    def update_nwg_insight(self, data, key):
        link = f"http://10.132.58.167/rest/insight/1.0/object/{key}/"
        headers = {'Content-type': 'application/json'}
        response = requests.put(link, auth=(self.insight_username, self.insight_password), data=json.dumps(data),
                                headers=headers, verify=False)
        print(response.status_code)
        print("Done.")

    def create_nwg_insight(self, data):
        link = "http://10.132.58.167/rest/insight/1.0/object/create/"
        headers = {'Content-type': 'application/json'}
        response = requests.post(link, auth=(self.insight_username, self.insight_password), data=json.dumps(data),
                                 headers=headers, verify=False)
        print(response.status_code)
        print("Done.")
