import os
import xml.etree.ElementTree as ET
import csv
from ftplib import FTP


ftp_server = 'IP'
username = "username"
passwd = "password"
ftp_directory = "/path/to/xml/oss/file"


def get_xmls(username, passwd, ftp_server, ftp_directory):
    ftp = FTP(ftp_server)
    ftp.login(user=username, passwd=passwd)
    ftp.cwd(ftp_directory)
    files_list = ftp.nlst()

    for file in files_list:
        with open(file, "wb") as f:
            print('downloading {}...'.format(file))
            ftp.retrbinary('RETR {}'.format(file), f.write)


def xml_to_csv(dictionary):
    # pprint(dictionary)

    keys_set = set()
    for key, datas in dictionary.items():
        for data in datas:
            for each in data:
                for i in each.keys():
                    keys_set.add(i)

    di = {}
    for key in keys_set:
        di[key] = ''
    for key, datas in dictionary.items():
        data = []
        for d in datas:
            for i in d:
                data.append(i)
        filename = f'{key}.csv'
        with open(filename, "w") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=keys_set)
            writer.writeheader()
            writer.writerows(data)


def parse_xml(xml_file):
    data_dictionary = {}

    trees = ET.parse(xml_file)
    for tree in trees.iter():
        tags = tree.tag
        # print(tags)

        tag_attributes = tree.attrib
        if tag_attributes.get('NEName'):
            identifier = tag_attributes.get('NEName')

        if tags == 'NE':
            # print(tag_attributes)
            data_dictionary['NE'] = [tag_attributes]

        if tags == 'TABLE':
            # print(table_attribute)
            table_attribute = tag_attributes.get('attrname')
            data_dictionary[table_attribute] = []
        if tags == 'ROW':
            # print(tag_attributes)
            tag_attributes.update({'Identifier': identifier})
            data_dictionary[table_attribute].append(tag_attributes)

        if tags == "MBTS":
            data_dictionary['MBTS'] = [tag_attributes]

        if tags == "BTS":
            data_dictionary['BTS'] = [tag_attributes]

        if tags == "BTS3900":
            data_dictionary['BTS3900'] = [tag_attributes]

    # pprint(data_dictionary)
    return data_dictionary


di = {}
test = {}

xml_path = os.getcwd()

for root, dirs, files in os.walk(xml_path):
    print("root ---> ", root)
    print("dir  ---> ", dirs)
    for file in files:
        if file.endswith(".xml"):
            file_path = os.path.join(root, file)
            print(file_path)
            dict_datas = parse_xml(file_path)
            di.update(dict_datas)

    for key in di.keys():
        try:
            if test[key]:
                pass
        except Exception as err:
            test[key] = []

    for file in files:
        if file.endswith(".xml"):
            file_path = os.path.join(root, file)
            print("-------> ", file_path)
            dict_datas = parse_xml(file_path)
            for key, value in dict_datas.items():
                test[key].append(value)

get_xmls(username, passwd, ftp_server, ftp_directory)
xml_to_csv(test)
