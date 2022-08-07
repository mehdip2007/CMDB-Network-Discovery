import re


version = {

    "hostname": re.compile(r"Hostname:\s(.+)"),
    "mode": re.compile(r"Model:\s(.+)?"),
    "version": re.compile(r"Junos:\s(\S+)")

}
