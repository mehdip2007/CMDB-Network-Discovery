from modules.dict_regex import inventory_regex
import pandas as pd
import os

cwd = os.getcwd()
path = "{}/inventory".format(cwd)
os.mkdir(path)
os.chdir(path)


def inventory_parser(output, prompt, host):
    def dict_to_dict(dictionary):
        df = pd.DataFrame.from_dict(dictionary, orient='index').T
        df['Host'] = prompt.replace("#", "")
        csv_result = '{}_Result.csv'.format(host)
        df.to_csv(csv_result, index=False)

    data_dictionary = {}
    name_list = []
    desc_list = []
    pid_list = []
    sn_list = []

    for key, regex in inventory_regex.items():
        matches = regex.findall(output)
        if matches:
            if key == "Name":
                for match in matches:
                    name_list.append(match)
            if key == "Description":
                for match in matches:
                    desc_list.append(match)
            if key == "PID":
                for match in matches:
                    pid_list.append(match)
            if key == "SN":
                for match in matches:
                    sn_list.append(match)

    data_dictionary['Name'] = name_list
    data_dictionary['Description'] = desc_list
    data_dictionary['PID'] = pid_list
    data_dictionary['SN'] = sn_list

    # print(data_dictionary)
    dict_to_dict(data_dictionary)
