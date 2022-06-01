from modules import check_connection
from modules.Cisco import Router
from modules import csv_merger
from modules.init_packages import os
from modules.Cisco import insight_object


def read_ip(ip_file_path,cisco_ip_filename):
    with open(ip_file_path, "r") as lines:
        ips = lines.read().split('\n')

    for ip in ips[:-1]:

        # Check the connection
        pinger = check_connection.Connection()
        pinger.check_ping(ip)

        # executing commands to fetch the data
        cisco = Router(host=ip, user=username, password=password, device_type=device_type)
        cisco.get_version(version_command,cisco_ip_filename)
        cisco.get_ip_init(ip_init_command,cisco_ip_filename)
        cisco.get_inventory(inventory_command,cisco_ip_filename)


# Basic Info and Commands
# Router Credentials
username = "user"
password = "password"

insight_username = 'user'
insight_password = 'pass'

device_type = "cisco_ios"
version_command = "show version"
ip_init_command = "show ip int brief"
inventory_command = "show inventory"

nwg = insight_object.NetworkInsightCreateUpdate(insight_username=insight_username,
                                                insight_password=insight_password)

# /data/finalizeDiscovery/2/NetworkDiscovery
ip_file_path_list = ["/data/finalizeDiscovery/2/NetworkDiscovery/cisco_ipran_ips.txt",
                     "/data/finalizeDiscovery/2/NetworkDiscovery/cisco_ipbb_ips.txt",
                     "/data/finalizeDiscovery/2/NetworkDiscovery/cisco_ips.txt"]


# put path of the all csv to merge all in one file
for ip_file_path in ip_file_path_list:
    cisco_ip_filename = os.path.basename(ip_file_path.strip('.txt').lower())
    read_ip(ip_file_path,cisco_ip_filename)
    print("Merging Version Files.....")
    csv_version_path = f"{os.getcwd()}/version"
    csv_merger.merge(csv_version_path, cisco_ip_filename) 
    print("Version Merge Done.")

    print("Merging Interface Files....")
    csv_ip_init_path = f"{os.getcwd()}/interface"
    csv_merger.merge(csv_ip_init_path, cisco_ip_filename)
    print("Interface Merge Done.")

    print("Merging Inventory Files....")
    csv_inventory_path = f"{os.getcwd()}/inventory"
    csv_merger.merge(csv_inventory_path, cisco_ip_filename)
    print("Inventory Merge Done.")

    # Inserting Data to NWG Insight
    data_path = path = os.getcwd()
    datas = os.listdir(data_path)
    for data in datas:
        if data.endswith(".csv"):
            print("Reading File ---->", data)
            if "version_cisco_ipran" in data:
                print("Getting IPRAN Info", data)
                cisco_insight_name = "CISCO IPRAN"
                print("**** IPRAN --->", cisco_insight_name)
                nwg.get_object_entires(cisco_insight_name)
                nwg.update_or_create_insight(data)
            if "version_cisco_ipbb" in data:
                print("Getting IPBB Info", data)
                cisco_insight_name = "Cisco IPBB"
                print("**** IPBB --->", cisco_insight_name)
                nwg.get_object_entires(cisco_insight_name)
                nwg.update_or_create_insight(data)
            if "cisco_ip_" in data:
                print("Getting Only Cisco", data)
                cisco_insight_name = "Cisco"
                print("**** Cisco --->", cisco_insight_name)
                nwg.get_object_entires(cisco_insight_name)
                nwg.update_or_create_insight(data)
