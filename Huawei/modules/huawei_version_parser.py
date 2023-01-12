from .huawei_dict_regex import version
import pandas as pd
import os
import huawei_csv_reader_insight_create_updater as insight

cwd = os.getcwd()
version_path = os.path.join(cwd, "huawei_version")
os.makedirs(version_path, exist_ok=True)


def version_parser(stdout, ip):
    data_dictionary = {'LPU': [], 'VRP': [], 'Version': [], 'PIC': [], 'MPU': [], 'SFU': [], 'PWR': [], 'FAN': [],
                       'PMU': [], 'CLK': [], 'CXP': [], 'Host': [], 'Uptime': [], 'IP': [ip]}

    for key, regex in version.items():
        matches = regex.findall(stdout)
        if matches:
            data_dictionary[key].append(matches[0])

    df = pd.DataFrame.from_dict(data_dictionary, orient="index").T
    df = df.fillna(value='-')
    df = df.rename({'Host': 'Name'})
    print("Generating CSV file for version command...")

    csv_file = os.path.join(version_path, "huawei_version_all.csv")

    # if file does not exist write header
    if not os.path.isfile(csv_file):
        df.to_csv(csv_file, header=[k for k, v in data_dictionary.items()], ignore_index=True)
    else:  # else it exists so append without writing the header
        df.to_csv(csv_file, mode='a', header=False, ignore_index=True)

    insight.reader(csv_file)
