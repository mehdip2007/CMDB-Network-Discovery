from modules.init_packages import os
from modules.init_packages import pandas as pd
from modules.init_packages import Path
from . import cisco_regex_dict

cwd = os.getcwd()
path = f"{cwd}/inventory"

# Check whether the specified path exists or not
isExist = os.path.exists(path)
if not isExist:
    # Create a new directory because it does not exist
    os.makedirs(path)
    print(f"The directory {path} is created!")
else:
    os.chdir(cwd)


def inventory_parser(output, prompt, cisco_type, host):
    
    Path(f"{path}/{cisco_type}").mkdir(parents=True, exist_ok=True)

    def dict_to_dict(dictionary):
        df = pd.DataFrame.from_dict(dictionary, orient='index').T
        df['Host'] = prompt.replace("#", "")
        csv_result = '{}/{}/{}_Result.csv'.format(path, cisco_type, host)
        df.to_csv(csv_result, index=False)

    data_dictionary = {}
    name_list = []
    desc_list = []
    pid_list = []
    sn_list = []
    ip_list = {host}

    for key, regex in cisco_regex_dict.inventory_regex.items():
        matches = regex.findall(output)
        if matches:
            if key == "Name":
                name_list.append(matches[0])
            if key == "Description":
                desc_list.append(matches[0])
            if key == "PID":
                pid_list.append(matches[0])
            if key == "SN":
                sn_list.append(matches[0])
            # if key == "IP":
            #     ip_list.append(matches[0])

    data_dictionary['Name'] = name_list
    data_dictionary['Description'] = desc_list
    data_dictionary['PID'] = pid_list
    data_dictionary['SN'] = sn_list
    data_dictionary['IP Address'] = list(ip_list)

    # print(data_dictionary)
    dict_to_dict(data_dictionary)
