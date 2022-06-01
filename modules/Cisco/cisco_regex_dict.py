from modules.init_packages import re


version_regex = {

    'IOS Software': re.compile(r"^.*Software\s\((\w+-\w+-\w+)\)"),
    'IOS Software2': re.compile(r"cisco\s(\w+-\w+-\w+)"),
    'Name': re.compile(r"(\w+-\w+-\w+) uptime\s+is\s+.+"),
    'Name2': re.compile(r"(\w+_\w+)\suptime\s+is\s+.+"),
    'Name3': re.compile(r"^\s(\w+-\w+)\suptime"),
    'Name4': re.compile(r"cisco\s(\w+-\w+-\w+)"),
    'Uptime': re.compile(r"uptime\sis\s(.*)"),
    'Version': re.compile(r"^.*Software\s.+\),\sVersion\s(.+?),*\s+RELEASE.*"),
    'Serial': re.compile(r"[Pp]rocessor\s+board\s+ID\s+(\S+)"),
    'Model': re.compile(r".*[cC]isco\s(\w+-\S+)"),
    'Memory': re.compile(r".*[cC]isco\s.*processor\s.*with\s(\S+)"),
    'CPU Clock': re.compile(r".*P2020\sCPU\sat\s(\d+\w+)"),
    'CPU Clock2': re.compile(r"\sCPU:(\w+Hz)"),
    'CPU Clock3': re.compile(r"CPU\sat\s(\w+Hz)"),
    'CPU Core': re.compile(r".*P2020\sCPU\sat\s\w+,\s(\S+)"),
    'CPU Core2': re.compile(r"CORE:\s(\w+)"),
    'CPU Model': re.compile(r".*[cC]isco\s\S+\s\((\w+)"),
    'IOS Release': re.compile(r"^Cisco.*RELEASE.+\((\w+)"),
    'MAC': re.compile(r"\w{2}:\w{2}:\w{2}:\w{2}:\w{2}:\w{2}"),
    'Nexus': re.compile(r"\s\scisco\s(\S+\s\w+)"),
    'Nexus Name': re.compile(r"\s\sDevice\sname:\s(\S+)"),
    'Nexus Version': re.compile(r"\s\ssystem:.*version\s(\S+)"),
    'Nexus CPU': re.compile(r"\s\s(Intel\S+\s\S+)\sCPU"),
    'IP': re.compile(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}")

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
