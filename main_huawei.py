from modules import connectivity_checker
from modules import huawei_version_parser as hvp
from modules import Ssh

user = "cmdb"
pwd = "arian#%FD20_20a"


pinger = connectivity_checker.Availability()
pinger.check_ping(hvp.ip)

ssh_client = Ssh(ip=hvp.ip, username=user, password=pwd, timeout=10)
get_version = ssh_client.display()
get_elabel = ssh_client.elabel_iptv()
get_phy_option = ssh_client.phy_options()
get_ip_init_brief = ssh_client.ip_init_brief()
# get_elabel = ssh_client.get_huawei_elabel()
