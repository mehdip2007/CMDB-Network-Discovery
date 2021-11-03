from modules import connectivity_checker
from modules.cisco_router import Router
import sys


ips = str(sys.argv[1])
username = "user"
password = "pass"
device_type = "cisco_ios"
version_command = "show version"
ip_init_command = "show ip int brief"
inventory_command = "show inventory"

pinger = connectivity_checker.Availability()
pinger.check_ping(ips)

cisco = Router(host=ips, user=username, password=password, device_type=device_type)
cisco.get_version(version_command)
cisco.get_ip_init(ip_init_command)
cisco.get_inventory(inventory_command)
