from cisco_dict_regex import inventory_regex
import pandas as pd
import os

cwd = os.getcwd()
path = "{}/inventory".format(cwd)
os.mkdir(path)
os.chdir(path)


def inventory_parser(output, prompt, host):
    def dict_to_dict(dictionary):
        df = pd.DataFrame.from_dict(dictionary, orient="index").T
        df["Host"] = prompt.replace("#", "")
        csv_result = "{}_Result.csv".format(host)
        df.to_csv(csv_result, index=False)

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
