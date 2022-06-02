import paramiko
import socket
from routing_table import get_routing_table

class Ssh:

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
                                look_for_keys=False, allow_agent=False)
            remote_shell = self.client.invoke_shell()
            print("Interactive SSH session established")
            return remote_shell
        except paramiko.AuthenticationException:
            print("Authentication failed, please verify your credentials")
        except paramiko.SSHException as sshException:
            print("Could not establish SSH connection: {}".format(sshException))
        except socket.timeout:
            print("Connection timed out")
        except Exception as e:
            print('\nException in connecting to the server', e)
            self.client.close()

    def get_ip_routing_table(self):
        get_routing_table(self.connect())
