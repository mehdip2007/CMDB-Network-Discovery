import re

version_regex = {

    'IOS Software': re.compile(r"^.*Software\s\((\w+-\w+-\w+)\)"),
    'Name': re.compile(r"(.*) uptime\s+is\s+.+"),
    'Uptime': re.compile(r"uptime\sis\s(.*)"),
    'Version': re.compile(r"^.*Software\s.+\),\sVersion\s(.+?),*\s+RELEASE.*"),
    'Serial': re.compile(r"[Pp]rocessor\s+board\s+ID\s+(\S+)"),
    'Model': re.compile(r".*[cC]isco\s(\w+-\S+)"),
    'Memory': re.compile(r".*[cC]isco\s.*processor\s.*with\s(\S+)"),
    'CPU Clock': re.compile(r".*P2020\sCPU\sat\s(\d+\w+)"),
    'CPU Core': re.compile(r".*P2020\sCPU\sat\s\w+,\s(\S+)"),
    'CPU Model': re.compile(r".*[cC]isco\s\S+\s\((\w+)"),
    'IOS Release': re.compile(r"^Cisco.*RELEASE.+\((\w+)"),
    'MAC': re.compile(r"\w{2}:\w{2}:\w{2}:\w{2}:\w{2}:\w{2}")

}

ip_int_regex = {

    'IP': re.compile(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"),
    'Vlan': re.compile(r"Vlan\S+"),
    'Gigabit': re.compile(r"[gG]iga\S+"),
    'Loopback': re.compile(r"[Ll]oop\S+")

}

inventory_regex = {

    'Name': re.compile(r"NAME:\s\"(.+?)\""),
    'Description': re.compile(r"DESCR:\s\"(.*)\""),
    'PID': re.compile(r"PID:\s(\S+)"),
    'SN': re.compile(r"SN:\s(\S+)")

}
