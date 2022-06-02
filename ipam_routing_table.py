import time
import re
from datetime import datetime
from vpn_vlan import vpn_vlan_id
import pandas as pd

# Regex for extraciting all IP addresses
ip_pattern = r"10{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\/\d+"
today = datetime.now().strftime("%Y-%m-%w")


# Create CSV for our data
def data_to_csv(data_dictionary, file_name):
    df = pd.DataFrame.from_dict(data_dictionary)
    df.to_csv("{}.csv".format(file_name), index=False)


#  Parse VRF data to CSV
def parsed_data(stdout, vpn_name, vrf_id):
    section_name = "VRF-{}".format(vrf_id).upper()
    data_dictionary = {"Section": section_name}
    ip_result = re.findall(ip_pattern, stdout)

    data_dictionary['Subnet'] = ip_result
    data_dictionary['Mask'] = ''
    data_dictionary['description'] = vpn_name
    data_dictionary['VLAN'] = ''
    data_dictionary['Domain'] = ''
    data_dictionary['VRF'] = "vrf-{}".format(vrf_id)
    data_dictionary['custom_Interface'] = ''
    data_dictionary['custom_VLAN-ID'] = ''
    # pprint(data_dictionary)

    file_name = "Result_{}_{}".format(vpn_name, vrf_id)
    data_to_csv(data_dictionary, file_name)


# After SSH need to generate the command screen for Device(HUAWEI) the get the stdout for parsing
def get_routing_table(remote_shell):
    for key, value in vpn_vlan_id.items():
        print("Getting Data from {}...".format(key))
        command = "screen-length 0 temporary \n display ip routing-table vpn-instance {} \n".format(key)
        remote_shell.send(command.encode() + b'\n')
        time.sleep(3)
        print("Recieving Data from Router...")
        stdout = remote_shell.recv(65000)
        stdout = stdout.decode().strip()
        parsed_data(stdout, key, value)
