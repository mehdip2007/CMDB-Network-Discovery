from cisco_dict_regex import version_regex
import os
import pandas as pd

cwd = os.path.dirname(os.path.abspath(__file__))
version_file_path = os.path.join(cwd, "version")
os.makedirs(version_file_path, exist_ok=True)


def version_parser(output, host):
    def data_to_csv(dictionary):
        df = pd.DataFrame.from_dict(dictionary, orient="index").T
        csv_result = os.path.join(version_file_path, host)
        df.to_csv(f"{csv_result}_Result.csv", index=False)

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
        "Version": "Cisco IOS Version'",
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
    }

    for key, regex in version_regex.items():
        matches = regex.findall(output)
        if matches:
            key = name_mapping[key]
            data_dictionary[key].append(matches[0])

    data_dictionary.update(
        {
            "CISCO IOS Software": data_dictionary["CISCO IOS Software"][:1],
            "Hostname": data_dictionary["Hostname"][:1],
        }
    )

    # print(data_dictionary)
    data_to_csv(data_dictionary)
    # return data_dictionary
