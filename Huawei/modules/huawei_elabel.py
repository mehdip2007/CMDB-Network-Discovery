import re
import json
import pandas as pd
import time


regex_dict = {
    'Slot#': re.compile(r"^[aA-zZ]+[0-9]|^[aA-zZ\s]+[0-9]+|^\d"),
    'BoardType': re.compile(r"^[a-zA-Z\s]+[0-9\s]+(.*?)\s|^\d\s(\w+-\d+\w+)"),
    'BarCode': re.compile(r"^[aA-zZ]+\s[0-9]+\s\w+\s(.*?)\s|^[aA-zZ]+[0-9]\s[aA-zZ\-0-9]+\s(.*?)\s"),
    'Description': re.compile(r"^[aA-zZ]+\s[0-9]+\s\w+\s.*?\s(\w.*)"),
    'Host': re.compile(r"<(.*)>"),
}

def get_huawei_elabel(remote_shell):
    command = "screen-length 0 temporary \n dis ip int brief \n".format()
    remote_shell.send(command.encode() + b'\n')
    time.sleep(5)

    print("Recieving Data from Router...")
    stdout = remote_shell.recv(65000)
    stdout = stdout.decode().strip()

    # print(stdout)
    # parse_elabel(stdout)
    return stdout