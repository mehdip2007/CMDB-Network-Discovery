import sys
import os
from dotenv import dotenv_values
from modules.cisco_router import Router
import modules.cisco_csv_reader_insight_create_updater as insight

"""
    Since there check_ping & merge method is out of the scope of this module i use get the current folder
    and add it's parent to sys.path to make it accessible.
"""
current = os.path.dirname(os.path.realpath(__file__))  # or os.path.dirname(os.path.abspath("__file__"))
parent = os.path.dirname(current)
sys.path.append(parent)
from connectivity_checker import check_ping
from csv_merger import merge


config = dotenv_values(os.path.join(parent, ".env"))
device_type = "cisco_ios"
version_command = "show version"
ip_init_command = "show ip int brief"
inventory_command = "show inventory"


cisco_ips = os.path.join(current, "cisco_ips.txt")
with open(cisco_ips, "r") as ips_file:
    ips = ips_file.readlines()

    for ip in ips:
        ip = ip.strip()
        try:
            if check_ping(ip):
                cisco = Router(host=ip, user=config.get('username'), password=config.get('password'),
                               device_type=device_type)
                cisco.get_version(version_command)
                cisco.get_ip_init(ip_init_command)
                cisco.get_inventory(inventory_command)
            else:
                print("Ping is not Available.")
        except KeyError as er:
            print(f" **** Key  --> {er.args[0]} <-- is not available. ****")

cisco_output = os.path.join(current, "cisco_version")
merge(cisco_output, cisco_ips.split('/')[-1].strip('.txt'))
insight.reader(os.path.join(cisco_output, "cisco_ips_all.csv"))

