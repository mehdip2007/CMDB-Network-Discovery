from xml.etree import ElementTree as ET
import pandas as pd
from datetime import datetime
import os
import re


def dict_to_csv(di, filename):
    print("Start Generating CSV ---> ")
    df = pd.DataFrame.from_dict(di, orient='index').T
    csv_file_name = re.search(r"export_INVENTORY_(\d+-\d+-\d+T\S+)_", filename).group(1)
    csv_export_path = re.search(r"(.*enm\d+)", filename).group(1)
    df.to_csv(f'{os.path.join(csv_export_path, csv_file_name)}.csv', index=False)


def xml_parser(file):
    print("Start Parsing XML ---> ", datetime.now())
    trees = ET.parse(file)

    d = {}
    serial_numbers = []
    inventory_unit_type = []
    vendor_unit_family_type = []
    vendor_unit_type_number = []
    vendor_name = []
    date_of_manufacture = []
    unit_position = []
    manufacturer_data = []
    managed_element = []
    inventory_unit = []

    for tree in trees.iter():
        tags = tree.tag
        # print(tags)
        if tags == '{http://www.3gpp.org/ftp/specs/archive/32_series/32.695#inventoryNrm}serialNumber':
            serial_numbers.append(tree.text)
        if tags == '{http://www.3gpp.org/ftp/specs/archive/32_series/32.695#inventoryNrm}inventoryUnitType':
            inventory_unit_type.append(tree.text)
        if tags == '{http://www.3gpp.org/ftp/specs/archive/32_series/32.695#inventoryNrm}vendorUnitFamilyType':
            vendor_unit_family_type.append(tree.text)
        if tags == '{http://www.3gpp.org/ftp/specs/archive/32_series/32.695#inventoryNrm}vendorUnitTypeNumber':
            vendor_unit_type_number.append(tree.text)
        if tags == '{http://www.3gpp.org/ftp/specs/archive/32_series/32.695#inventoryNrm}vendorName':
            vendor_name.append(tree.text)
        if tags == '{http://www.3gpp.org/ftp/specs/archive/32_series/32.695#inventoryNrm}dateOfManufacture':
            date_of_manufacture.append(tree.text)
        if tags == '{http://www.3gpp.org/ftp/specs/archive/32_series/32.695#inventoryNrm}unitPosition':
            unit_position.append(tree.text)
        if tags == '{http://www.3gpp.org/ftp/specs/archive/32_series/32.695#inventoryNrm}manufacturerData':
            manufacturer_data.append(tree.text)
        if tags == '{http://www.3gpp.org/ftp/specs/archive/32_series/32.625#genericNrm}ManagedElement':
            for k, v in tree.attrib.items():
                managed_element.append(v)
        if tags == '{http://www.3gpp.org/ftp/specs/archive/32_series/32.695#inventoryNrm}InventoryUnit':
            for k, v in tree.attrib.items():
                inventory_unit.append(v)

    d['Serial Number'] = serial_numbers
    d['Inventory Unit Type'] = inventory_unit_type
    d['Vendor Unit Family Type'] = vendor_unit_family_type
    d['Vendor Unit Type Number'] = vendor_unit_type_number
    d['Vendor Name'] = vendor_name
    d['Date of Manufacture'] = date_of_manufacture
    d['Unit Position'] = unit_position
    d['Manufacturer Data'] = manufacturer_data
    d['Inventory Unit'] = inventory_unit
    d['Managed Element ID'] = managed_element

    # print(d)
    file_name_without_extension = os.path.splitext(file)[0]
    dict_to_csv(d, f'{file_name_without_extension}')
    print("End ---> ", datetime.now())
