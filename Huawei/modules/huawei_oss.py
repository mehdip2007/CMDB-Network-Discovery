from ftplib import FTP
import xml.etree.ElementTree as ET
import csv
import os


def get_xmls(username, passwd, ftp_server, ftp_directory):
    ftp = FTP(ftp_server)
    ftp.login(user=username, passwd=passwd)
    ftp.cwd(ftp_directory)
    # ftp.retrlines('LIST'
    files_list = ftp.nlst()

    for file in files_list:
        with open(file, "wb") as f:
            print('downloading {}...'.format(file))
            ftp.retrbinary('RETR {}'.format(file), f.write)


def get_identifier(dictionary):
    ne_items = dictionary["NE"]

    identifier = ""
    for item in ne_items:
        identifier = item.get('NEName')

    ident = {'Identifier': identifier}
    # print(ident)
    xml_to_csv(dictionary, ident)
    return ident


def xml_to_csv(dictionary, ident):
    header = set()
    for outer_key, outer_val in dictionary.items():
        for val in outer_val:
            for k, v in val.items():
                header.add(k)

    dictionary['Identifier'] = ident
    # pprint(dictionary)

    for outer_key, outer_val in dictionary.items():
        if outer_key != "Identifier":
            for each in outer_val:
                each['Identifier'] = ident["Identifier"]

            actual_file = "{}.csv".format(outer_key)

            if not os.path.isfile(actual_file):
                with open(actual_file, 'w') as file:
                    writer = csv.DictWriter(file, fieldnames=[k for k, v in outer_val[0].items()],
                                            quoting=csv.QUOTE_NONNUMERIC)
                    writer.writeheader()
                    writer.writerows(outer_val)
            else:
                with open(actual_file, 'a') as file:
                    writer = csv.DictWriter(file, fieldnames=[k for k, v in outer_val[0].items()],
                                            quoting=csv.QUOTE_NONNUMERIC)
                    writer.writerows(outer_val)


def xml_attributes(file):
    data_dictionary = {}

    tree = ET.parse(file)
    root = tree.getroot()

    for child in root:
        # tags = child.tag  # NE, TABLES
        if child.attrib:
            _1st_child = child.attrib
            data_dictionary['NE'] = [_1st_child]
        else:
            for tag in child.findall('TABLE'):
                table_attrname = tag.get('attrname')
                data_dictionary[table_attrname] = []

                for row in tag.findall('ROWDATA/ROW'):
                    row_data = row.attrib
                    data_dictionary[table_attrname].append(row_data)

    get_identifier(data_dictionary)
    return data_dictionary
