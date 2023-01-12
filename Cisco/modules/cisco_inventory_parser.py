from .cisco_dict_regex import inventory_regex
import pandas as pd
import os

cwd = os.getcwd()
inventory_path = os.path.join(cwd, 'inventory')
os.makedirs(inventory_path, exist_ok=True)


def inventory_parser(output, prompt, host):
    def dict_to_dict(dictionary):
        df = pd.DataFrame.from_dict(dictionary, orient="index").T
        df["Host"] = prompt.replace("#", "")
        df.to_csv(os.path.join(inventory_path, f"{host}_Result.csv"), index=False)

    data_dictionary = {
        "Name": [],
        "Description": [],
        "PID": [],
        "SN": [],
    }

    for key, regex in inventory_regex.items():
        matches = regex.findall(output)
        if matches:
            data_dictionary[key].extend(matches)

    # print(data_dictionary)
    dict_to_dict(data_dictionary)
