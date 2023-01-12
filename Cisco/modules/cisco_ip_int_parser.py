from .cisco_dict_regex import ip_int_regex
import os


cwd = os.getcwd()
interface_path = os.path.join(cwd, "interface")
os.makedirs(interface_path, exist_ok=True)


def ip_int_parser(output, prompt, host):
    with open(os.path.join(interface_path, f"{host}_ip_interface_result.csv"), "w") as file:
        regex = ip_int_regex.get("IP")
        matches = regex.findall(output)
        if matches:
            ips = "||".join(matches)
            file.write("Host,IPs" + '\n')
            file.write(os.path.join(interface_path, f"{prompt},{ips}" + '\n'))
