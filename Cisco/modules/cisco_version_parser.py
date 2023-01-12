from .cisco_dict_regex import version_regex
import os
import pandas as pd

os.makedirs("cisco_version", exist_ok=True)


def version_parser(output, host):

    """
        As there are multiple version output for cisco with also there are multiple key for their regexes.
        therefore mapping is created since our data dictionary has only one key with similar data.

    """

    data_dictionary = {
        "CISCO IOS Software": [],
        "Hostname": [],
        "IP Address": [host],
        "Uptime": [],
        "Cisco IOS Version": [],
        "Serial Number": [],
        "Device Model": [],
        "Memory": [],
        "CPU Clock rate": [],
        "CPU Core": [],
        "CPU Model": [],
        "IOS Release Software": [],
        "MAC Address": [],
    }

    name_mapping = {
        "IOS Software": "CISCO IOS Software",
        "IOS Software2": "CISCO IOS Software",
        "Name": "Hostname",
        "Name2": "Hostname",
        "Name3": "Hostname",
        "Name4": "Hostname",
        "Uptime": "Uptime",
        "Version": "Cisco IOS Version",
        "Serial": "Serial Number",
        "Model": "Device Model",
        "Memory": "Memory",
        "CPU Clock": "CPU Clock rate",
        "CPU Clock2": "CPU Clock rate",
        "CPU Clock3": "CPU Clock rate",
        "CPU Core": "CPU Core",
        "CPU Core2": "CPU Core",
        "CPU Model": "CPU Model",
        "IOS Release": "IOS Release Software",
        "MAC": "MAC Address",
        "Nexus": "CISCO IOS Software",
        "Nexus Name": "Hostname",
        "Nexus Version": "Cisco IOS Version",
        "Nexus CPU": "CPU Model",
        "IP": "IP",
    }

    # iterate over our regex dictionary to map the key and its corresponding value of its regex.
    for key, regex in version_regex.items():
        matches = regex.findall(output)
        if matches:
            key = name_mapping[key]
            data_dictionary[key].append(matches[0])

    # since there are two value with the same result in out list for its key we get the fist one
    data_dictionary.update(
        {
            "CISCO IOS Software": data_dictionary["CISCO IOS Software"][:1],
            "Hostname": data_dictionary["Hostname"][:1],
            "CPU Clock rate": data_dictionary["CPU Clock rate"][:1],
        }
    )

    # data_to_csv(data_dictionary)
    df = pd.DataFrame.from_dict(data_dictionary, orient="index").T
    df.rename(columns={'Hostname': 'Name'}, inplace=True)
    csv_result = os.path.join("cisco_version", host)
    df.to_csv(f"{csv_result}_Result.csv", index=False)
