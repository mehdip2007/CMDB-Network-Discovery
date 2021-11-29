import socket
import paramiko
from modules.juniper_chassis_result import get_chassis_result
from modules.juniper_version import get_version_info
import re


class Router:

    def __init__(self, ip, username, password, timeout):
        self.ssh_output = None
        self.ssh_error = None
        self.client = None
        self.ip = ip
        self.username = username
        self.password = password
        self.timeout = float(timeout)

    def connect(self):
        """Login to the remote server"""
        try:
            # Paramiko.SSHClient can be used to make connections to the remote server and transfer files
            print("Establishing ssh connection")
            self.client = paramiko.SSHClient()
            # Parsing an instance of the AutoAddPolicy to set_missing_host_key_policy() changes it to allow any host.
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.client.connect(hostname=self.ip, username=self.username, password=self.password,
                                look_for_keys=False, allow_agent=False, banner_timeout=200)
            return True
        except paramiko.AuthenticationException:
            print("Authentication failed, please verify your credentials")
        except paramiko.SSHException as sshException:
            print("Could not establish SSH connection: {}".format(sshException))
        except socket.timeout:
            print("Connection timed out")
        except Exception as e:
            print('\nException in connecting to the server', e)
            self.client.close()

    def get_chassis_slots(self):
        command = "show chassis fpc "
        if self.connect():
            stdin, stdout, stderr = self.client.exec_command(command, timeout=10)
            stdout = stdout.read().decode('utf-8')
            # print(stdout)

            online_pattern = r"\s\s(\d+)\s\sOnline"
            online_slot = re.search(online_pattern, stdout)
            online_slot = online_slot.group(1)

            offline_pattern = r"\s\s(\d+)\s\sEmpty"
            offline_slot = re.findall(offline_pattern, stdout)

            remote_shell = self.client.invoke_shell()
            get_chassis_result(online_slot, offline_slot, remote_shell, self.ip)

    def get_version(self):
        device_info = {
            'device_type': 'juniper_junos',
            'host': str(self.ip),
            'username': self.username,
            'password': self.password,
            'port': 22,  # optional, defaults to 22
        }
        get_version_info(device_info)

