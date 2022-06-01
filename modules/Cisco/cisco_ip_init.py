from modules.init_packages import os
from . import cisco_regex_dict


cwd = os.getcwd()
path = f"{cwd}/interface"

# Check whether the specified path exists or not
isExist = os.path.exists(path)
if not isExist:
    # Create a new directory because it does not exist
    os.makedirs(path)
    print(f"The directory {path} is created!")
else:
    # os.chdir(f"../{cwd}")
    os.chdir(cwd)


def ip_init_parser(output, prompt, cisco_type, host):
    with open("{}/{}/{}_ip_interface_result.csv".format(path, cisco_type, host), "w") as file:
        for key, regex in cisco_regex_dict.ip_int_regex.items():
            matches = regex.findall(output)
            if matches:
                if key == 'IP':
                    ips = "||".join(matches)
                    file.write("Host,IPs" + '\n')
                    file.write("{},{}".format(prompt, ips) + '\n')
