import re

phy_option = {

    'Host': re.compile(r"<(.*)>"),
    'Interface': re.compile(r"(giga.*)", re.IGNORECASE),
    'Vendor_PN': re.compile(r"the vendor PN is (.*)", re.IGNORECASE),
    'Transceiver': re.compile(r"(Transceiver BW.*)", re.IGNORECASE),
}


elabel = {
    'Slot#': re.compile(r"^[aA-zZ]+[0-9]|^[aA-zZ\s]+[0-9]+|^\d"),
    'BoardType': re.compile(r"^[a-zA-Z\s]+[0-9\s]+(.*?)\s|^\d\s(\w+-\d+\w+)"),
    'BarCode': re.compile(r"^[aA-zZ]+\s[0-9]+\s\w+\s(.*?)\s|^[aA-zZ]+[0-9]\s[aA-zZ\-0-9]+\s(.*?)\s"),
    'Description': re.compile(r"^[aA-zZ]+\s[0-9]+\s\w+\s.*?\s(\w.*)"),
    'Host': re.compile(r"<(.*)>"),
}


version = {
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


elable_iptv = {

    'Slots': re.compile(r"^[aA0-zZ9]+\s\d+|^PM\d"),
    'BoardType': re.compile(r"^\w+\s\d+\s(\w+)|^\w+\d\s(\w+-\w+)?"),
    'BarCode': re.compile(r"^\w+\s\d+\s\w+\s(\d+\w+)|^\w+\d\s\w+-\w+\s(\d+\w+)"),
    'Description': re.compile(r"^\w+\s\d+\s\w+\s\d+\w+\s(\w+-.*|[0-9]+.*)"),
    'Host': re.compile(r"<(.*)>")

}


ip_init_brief = {
        'Host': re.compile(r"<(.*)>"),
        'IPs':  re.compile(r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})")
}



