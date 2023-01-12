from dotenv import dotenv_values
import os
import sys
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
from connectivity_checker import check_ping
from modules.huawei_router import Router


config = dotenv_values("../.env")
version_command = "screen-length 0 temporary \n display version \n"
ip_init_command = "display ip int brief"
inventory_command = "display inventory"

huawei_ipbb_ips = os.path.join(current, "Huawei-IPBB")
with open(huawei_ipbb_ips, "r") as ips_file:
    ips = ips_file.readlines()

    for ip in ips:
        ip = ip.strip()
        try:
            if check_ping(ip):
                huawei = Router(ip=ip, username=config.get('username'), password=config.get('password'), timeout=10)
                huawei.get_version(version_command, ip)
                huawei.get_ip_init(ip_init_command)
                huawei.get_inventory(inventory_command)
            else:
                print("Ping is not Available.")
        except KeyError as er:
            print(f" **** Key  --> {er.args[0]} <-- is not available. ****")

