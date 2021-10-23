import time
import re
import pandas as pd
import numpy as np
import sys

regex_dict = {

    'Host': re.compile(r"<(.*)>"),
    'Interface': re.compile(r"(giga.*)", re.IGNORECASE),
    'Vendor_PN': re.compile(r"the vendor PN is (.*)", re.IGNORECASE),
    'Transceiver': re.compile(r"(Transceiver BW.*)", re.IGNORECASE),
}


ip = str(sys.argv[1])


def phy_option_to_csv(dictionary):
    print("Generating CSV file for version command...")
    df = pd.DataFrame.from_dict(dictionary, orient='index').T
    host = dictionary.get('Host')
    df[df['Host'] == ""] = np.NaN
    host = "".join(host)
    df[['Host']] = df[['Host']].fillna(value=str(host))
    df.to_csv("{}_phy_option_result.csv".format(ip), index=False)
    print("Generating CSV file is finished.")


def parse_phy_option_result(stdout):
    data_dictionary = {}
    hosts = set()
    interfaces = []
    vendor_pns = []
    transceiver = []

    for key, regex in regex_dict.items():
        matches = regex.findall(stdout)
        if matches:
            for match in matches:
                if key == 'Host':
                    hosts.add(match.strip())
                if key == 'Interface':
                    interfaces.append(match.strip())
                if key == 'Vendor_PN':
                    vendor_pns.append(match.strip())
                if key == 'Transceiver':
                    transceiver.append(match.strip())

    data_dictionary['Host'] = list(hosts)
    data_dictionary['Interface'] = interfaces
    data_dictionary['Vendor PN'] = vendor_pns
    data_dictionary['Transceiver'] = transceiver
    phy_option_to_csv(data_dictionary)


def get_huawei_phy_option(remote_shell):
    command = "screen-length 0 temporary \n display interface phy-option \n".format()
    remote_shell.send(command.encode() + b'\n')
    time.sleep(5)

    print("Recieving Data from Router...")
    stdout = remote_shell.recv(65000)
    stdout = stdout.decode().strip()

    # print(stdout)
    parse_phy_option_result(stdout)
    return stdout
