import paramiko
import socket
from modules import huawei_version_parser as hvp
from modules import huawei_elabel_iptv as hei
from modules import huawei_phy_option as hpo
from modules import huawei_ip_init_brief as hip
from modules import huawei_elabel


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

    def display(self):
        hvp.get_huawei_version(self.connect())

    def elabel_iptv(self):
        hei.get_huawei_iptv_elabel(self.connect())

    def phy_options(self):
        hpo.get_huawei_phy_option(self.connect())

    def ip_init_brief(self):
        hip.get_huawei_ip_init_brief(self.connect())

    # def elabel(self):
    #     huawei_elabel.get_huawei_elabel(self.connect())

