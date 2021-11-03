from netmiko import ConnectHandler

from modules.cisco_inventory_parser import inventory_parser
from modules.cisco_ip_int_parser import ip_int_parser
from modules.cisco_version_parser import version_parser


class Router:

    def __init__(self, host, user, password, device_type):
        self.host = host
        self.user = user
        self.password = password
        self.device_type = device_type

        self.device_info = {
            'device_type': self.device_type,
            'host': str(self.host),
            'username': self.user,
            'password': self.password,
            'port': 22,          # optional, defaults to 22
        }

    def get_version(self, command):
        with ConnectHandler(**self.device_info) as net_connect:
            # Use TextFSM to retrieve structured data
            # output = net_connect.send_command(command, use_textfsm=True)
            result = net_connect.send_command(command)

        version_parser(result)

    def get_ip_init(self, command):
        with ConnectHandler(**self.device_info) as net_connect:
            prompt = net_connect.find_prompt()
            result = net_connect.send_command(command)

        ip_int_parser(result, prompt, self.host)

    def get_inventory(self, command):
        with ConnectHandler(**self.device_info) as net_connect:
            prompt = net_connect.find_prompt()
            result = net_connect.send_command(command)

        inventory_parser(result, prompt, self.host)
