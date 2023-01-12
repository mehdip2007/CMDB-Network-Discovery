import paramiko
import socket
import time
from .huawei_version_parser import version_parser


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
                                look_for_keys=False, allow_agent=False)
            print("Interactive SSH session established")
            return self.client.invoke_shell()
        except paramiko.AuthenticationException:
            print("Authentication failed, please verify your credentials")
        except paramiko.SSHException as sshException:
            print("Could not establish SSH connection: {}".format(sshException))
        except socket.timeout:
            print("Connection timed out")
        except Exception as e:
            print('\nException in connecting to the server', e)
            self.client.close()

    def get_version(self, version_command, ip):
        remote_shell = self.connect()
        if remote_shell:
            remote_shell.send(version_command.encode() + b'\n')
            time.sleep(5)

            print("Recieving Data from Router...")
            stdout = remote_shell.recv(65000)
            stdout = stdout.decode().strip()

            version_parser(stdout, ip)
            return stdout
