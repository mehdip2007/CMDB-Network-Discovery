from dotenv import dotenv_values
import nwg_cmdb.connectivity_checker
from modules.cisco_router import Router
import sys


ips = str(sys.argv[1])
config = dotenv_values("../.env")
device_type = "cisco_ios"
version_command = "show version"
ip_init_command = "show ip int brief"
inventory_command = "show inventory"

if check_ping(ips):
    cisco = Router(host=ips, user=config.get('username'), password=config.get('password'), device_type=device_type)
    cisco.get_version(version_command)
    # cisco.get_ip_init(ip_init_command)
    # cisco.get_inventory(inventory_command)
else:
    print("Ping is not Available.")



