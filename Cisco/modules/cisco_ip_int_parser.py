from cisco_dict_regex import ip_int_regex
import os


cwd = os.getcwd()
path = "{}/interface".format(cwd)
os.mkdir(path)
os.chdir(path)


def ip_int_parser(output, prompt, host):
    with open(f"{host}_ip_interface_result.csv", "w") as file:
        for key, regex in ip_int_regex.items():
            regex = ip_int_regex.get("IP")
            matches = regex.findall(output)
            if matches:
                ips = "||".join(matches)
                file.write("Host,IPs" + '\n')
                file.write(f"{prompt},{ips}" + '\n')
            
        