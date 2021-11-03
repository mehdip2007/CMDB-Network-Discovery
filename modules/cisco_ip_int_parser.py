from modules.dict_regex import ip_int_regex
import os


cwd = os.getcwd()
path = "{}/interface".format(cwd)
os.mkdir(path)
os.chdir(path)


def ip_int_parser(output, prompt, host):
    with open("{}_ip_interface_result.csv".format(host), "w") as file:
        for key, regex in ip_int_regex.items():
            matches = regex.findall(output)
            if matches:
                if key == 'IP':
                    ips = "||".join(matches)
                    file.write("Host,IPs" + '\n')
                    file.write("{},{}".format(prompt, ips) + '\n')
