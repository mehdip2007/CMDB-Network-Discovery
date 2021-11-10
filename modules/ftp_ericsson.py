import paramiko
import socket
import os

class Ssh:

    def __init__(self, host, username, password, timeout, port):
        self.ssh_output = None
        self.ssh_error = None
        self.client = None
        self.host = host
        self.username = username
        self.password = password
        self.timeout = float(timeout)
        self.port = port

    def connect(self):
        """Login to the remote server"""
        try:
            # Paramiko.SSHClient can be used to make connections to the remote server and transfer files
            print("Establishing ssh connection")
            self.client = paramiko.SSHClient()
            # Parsing an instance of the AutoAddPolicy to set_missing_host_key_policy() changes it to allow any host.
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.client.connect(hostname=self.host, username=self.username, password=self.password,
                                look_for_keys=False, allow_agent=False, port=self.port)
            print("SSH session established")
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

    def download_files(self):
        remote_path = "/home/shared/DATA/ENM-HWInventory"
        pattern = "'*.zip'"
        rawcommand = "find {remote_path} -name {pattern}"
        command = rawcommand.format(remote_path=remote_path, pattern=pattern)

        if self.connect():
            stdin, stdout, stderr = self.client.exec_command(command, get_pty=True)
            file_list = stdout = stdout.read().splitlines()

            ftp = self.client.open_sftp()
            for file in file_list:
                file = file.decode("utf-8")
                (head, filename) = os.path.split(file)
                ftp.get(file, './' + filename)

            ftp.close()
            self.client.close()
