import time
import re
import sys

pattern = {
        'Host': re.compile(r"<(.*)>"),
        'IPs':  re.compile(r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})")
}

input_ip = str(sys.argv[1])


def ip_brief_to_csv(dictionary):
    print("Generating CSV file for version command...")
    host_ips = dictionary.get('IPs')
    host_ips = "|".join(host_ips)
    host_name = dictionary.get('Host')
    host_name = "".join(host_name)

    filename = "{}_ip_init_brief.csv".format(input_ip)
    with open(filename, 'w') as f:
        f.write("Host_Name,IPs" + '\n')
        f.write("{},{}".format(host_name, host_ips) + '\n')


def parse_ip_brief(stdout):
    data_dictionary = {}
    ips_list = []
    host = set()

    for key, regex in pattern.items():
        matches = regex.findall(stdout)
        if matches:
            for match in matches:
                if key == 'Host':
                    host.add(match.strip())
                if key == 'IPs':
                    ips_list.append("".join(match))

    data_dictionary['Host'] = host
    data_dictionary['IPs'] = ips_list
    ip_brief_to_csv(data_dictionary)


def get_huawei_ip_init_brief(remote_shell):
    command = "screen-length 0 temporary \n dis ip int brief \n".format()
    remote_shell.send(command.encode() + b'\n')
    time.sleep(5)

    print("Recieving Data from Router...")
    stdout = remote_shell.recv(65000)
    stdout = stdout.decode().strip()

    # print(stdout)
    parse_ip_brief(stdout)
    return stdout
