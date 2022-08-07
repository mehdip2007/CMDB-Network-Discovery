import time
import re
import pandas as pd
import numpy as np
import sys


version_regex = {
         'LPU': re.compile(r"LPU\s(.*?):.*(uptime.*)"),
         'VRP': re.compile(r"VRP.*(Version.\d.\d+)"),
         'Version': re.compile(r"HUAWEI (\w+.*)(uptime.*)"),
         'PIC': re.compile(r"PIC\s\d.*(uptime.*)"),
         'MPU': re.compile(r"MPU\s(.*?):.*(uptime.*)"),
         'SFU': re.compile(r"SFU\s(.*?):.*(uptime.*)"),
         'PWR': re.compile(r"PWR\s\d.*(uptime.*)"),
         'FAN': re.compile(r"FAN\s\d.*(uptime.*)"),
         'PMU': re.compile(r"PMU\s\d.*(uptime.*)"),
         'CLK': re.compile(r"CLK\s(.*?):.*(uptime.*)"),
         'CXP': re.compile(r"CXP\s\d.*(uptime.*)"),
         'Host': re.compile(r"<(.*)>"),
         # 'IP': re.compile(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}")
}

ip = str(sys.argv[1])


def version_to_csv(dictionary):
    print("Generating CSV file for version command...")
    df = pd.DataFrame.from_dict(dictionary, orient='index').T
    df['IP'] = ip
    host = dictionary.get('Host')
    df[df['Host'] == ""] = np.NaN
    host = "".join(host)
    df[['Host']] = df[['Host']].fillna(value=str(host))
    df.to_csv("{}_version_result.csv".format(ip), index=False)
    print("Generating CSV file is finished.")


def parse_version_result(stdout):
    data_dictionary = {}
    lpu_list = []
    pic_list = []
    sfu_list = []
    pwr_list = []
    fan_list = []
    pmu_list = []
    clk_list = []
    cxp_list = []
    mpu_list = []
    vrp_list = []
    hosts_list = set()

    for key, regex in version_regex.items():
        matches = regex.findall(stdout)
        if matches:
            if key == 'LPU':
                for match in matches:
                    result = " ".join(match)
                    lpu_list.append(result.strip())
            if key == 'MPU':
                for match in matches:
                    result = " ".join(match)
                    mpu_list.append(result.strip())
            if key == 'PIC':
                for match in matches:
                    pic_list.append(match.strip())
            if key == 'SFU':
                for match in matches:
                    result = " ".join(match)
                    sfu_list.append(result.strip())
            if key == 'PWR':
                for match in matches:
                    pwr_list.append(match.strip())
            if key == 'FAN':
                for match in matches:
                    fan_list.append(match.strip())
            if key == 'PMU':
                for match in matches:
                    pmu_list.append(match.strip())
            if key == 'CLK':
                for match in matches:
                    result = " ".join(match)
                    clk_list.append(result.strip())
            if key == 'CXP':
                for match in matches:
                    cxp_list.append(match.strip())
            if key == 'Host':
                for match in matches:
                    hosts_list.add(match)
            if key == 'VRP':
                for match in matches:
                    vrp_list.append(match)

    data_dictionary['LPU'] = lpu_list
    data_dictionary['MPU'] = mpu_list
    data_dictionary['PIC'] = pic_list
    data_dictionary['SFU'] = sfu_list
    data_dictionary['PWR'] = pwr_list
    data_dictionary['FAN'] = fan_list
    data_dictionary['PMU'] = pmu_list
    data_dictionary['CLK'] = clk_list
    data_dictionary['CXP'] = cxp_list
    data_dictionary['VRP'] = vrp_list
    data_dictionary['Host'] = hosts_list
    # print(data_dictionary)
    version_to_csv(data_dictionary)


def get_huawei_version(remote_shell):
    command = "screen-length 0 temporary \n display version \n".format()

    remote_shell.send(command.encode() + b'\n')
    time.sleep(5)

    print("Recieving Data from Router...")
    stdout = remote_shell.recv(65000)
    stdout = stdout.decode().strip()

    # print(stdout)
    parse_version_result(stdout)
    return stdout
