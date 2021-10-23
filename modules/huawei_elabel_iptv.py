import time
import re
import pandas as pd
import numpy as np
import sys


regex_dict = {

    'Slots': re.compile(r"^[aA0-zZ9]+\s\d+|^PM\d"),
    'BoardType': re.compile(r"^\w+\s\d+\s(\w+)|^\w+\d\s(\w+-\w+)?"),
    'BarCode': re.compile(r"^\w+\s\d+\s\w+\s(\d+\w+)|^\w+\d\s\w+-\w+\s(\d+\w+)"),
    'Description': re.compile(r"^\w+\s\d+\s\w+\s\d+\w+\s(\w+-.*|[0-9]+.*)"),
    'Host': re.compile(r"<(.*)>")

}

ip = str(sys.argv[1])


def elabel_iptv_to_csv(dictionary):
    print("Generating CSV file for version command...")
    df = pd.DataFrame.from_dict(dictionary, orient='index').T
    df['IP'] = ip
    host = dictionary.get('Host')
    df[df['Host'] == ""] = np.NaN
    host = "".join(host)
    df[['Host']] = df[['Host']].fillna(value=str(host))
    df.to_csv("{}_elabel_iptv_result.csv".format(ip), index=False)
    print("Generating CSV file is finished.")


def parse_iptv_elabel_result(stdout):
    data_dictionary = {}
    hosts = set()
    boardtype = []
    slots = []
    description = []

    slots_lines_reg = re.compile("LPU.*|PIC.*|MPU.*|SFU.*|PM.*|FAN.*|PMU.*|<.*>")
    datas = slots_lines_reg.findall(stdout)
    if datas:
        for data in datas:
            data = data.strip()
            for key, regex in regex_dict.items():
                matches = regex.findall(data)
                if matches:
                    if key == 'Slots':
                        for match in matches:
                            slots.append(match)
                    if key == 'BoardType':
                        for match in matches:
                            match = "".join(match)
                            boardtype.append(match)
                    if key == 'Description':
                        for match in matches:
                            description.append(match)
                    if key == 'Host':
                        for match in matches:
                            hosts.add(match)

    data_dictionary['Host'] = hosts
    data_dictionary['Slots#'] = slots
    data_dictionary['BoardType'] = boardtype
    data_dictionary['Description'] = description
    elabel_iptv_to_csv(data_dictionary)


def get_huawei_iptv_elabel(remote_shell):
    command = "screen-length 0 temporary \n dis elabel brief \n".format()
    remote_shell.send(command.encode() + b'\n')
    time.sleep(5)

    print("Recieving Data from Router...")
    stdout = remote_shell.recv(65000)
    stdout = stdout.decode().strip()
    stdout = re.sub(' +', ' ', stdout)

    # print(stdout)
    parse_iptv_elabel_result(stdout)
    return stdout
