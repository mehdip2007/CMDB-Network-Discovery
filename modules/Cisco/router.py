from modules.init_packages import netmiko
from . import cisco_version
from . import cisco_ip_init
from . import cisco_inventory


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

    def get_version(self, command, cisco_type):
        with netmiko.ConnectHandler(**self.device_info) as net_connect:
            # Use TextFSM to retrieve structured data
            # output = net_connect.send_command(command, use_textfsm=True)
            result = net_connect.send_command(command)

        cisco_version.version_parser(result, cisco_type, self.host)

    def get_ip_init(self, command, cisco_type):
        with netmiko.ConnectHandler(**self.device_info) as net_connect:
            prompt = net_connect.find_prompt()
            result = net_connect.send_command(command)

        cisco_ip_init.ip_init_parser(result, prompt, cisco_type, self.host)

    def get_inventory(self, command, cisco_type):
        with netmiko.ConnectHandler(**self.device_info) as net_connect:
            prompt = net_connect.find_prompt()
            result = net_connect.send_command(command)

        cisco_inventory.inventory_parser(result, prompt, cisco_type, self.host)
