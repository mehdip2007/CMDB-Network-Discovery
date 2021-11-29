from modules import connectivity_checker
from modules.juniper_ssh import Router
import sys

ips = str(sys.argv[1])
username = "username"
password = "password"


pinger = connectivity_checker.Availability()
pinger.check_ping(ips)

juniper = Router(ip=ips, username=username, password=password, timeout=30)
# juniper.get_chassis_slots()
juniper.get_version()
