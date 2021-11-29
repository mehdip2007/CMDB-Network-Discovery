from netmiko import ConnectHandler
from pprint import pprint
import re
import pandas as pd

pattrens = {

    "hostname": re.compile(r"Hostname:\s(.+)"),
    "mode": re.compile(r"Model:\s(.+)?"),
    "version": re.compile(r"Junos:\s(\S+)")

}


host_list = []
mode_list = []
version_list = []
data_dictionary = {}


def get_version_info(device_info):

    def dict_to_csv(dictionary):
        df = pd.DataFrame.from_dict(dictionary)
        df.to_csv("{}_version_result.csv".format(device_info['host']), index=False)

    command = "show version"
    with ConnectHandler(**device_info) as net_connect:
        prompt = net_connect.find_prompt()
        result = net_connect.send_command(command)

        for key, regex in pattrens.items():
            matches = regex.search(result)
            if matches:
                if key == "hostname":
                    hostname = matches.group(1)
                    host_list.append(hostname)
                if key == "mode":
                    mode = matches.group(1)
                    mode_list.append(mode)
                if key == "version":
                    version = matches.group(1)
                    version_list.append(version)

    data_dictionary["Host"] = host_list
    data_dictionary["Version"] = version_list
    data_dictionary["mode"] = mode_list
    # pprint(data_dictionary)
    dict_to_csv(data_dictionary)
