import paramiko
import socket
import os
from zipfile import ZipFile
from xmlparser_csvgenerator import xml_parser


class Sftp:
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

    def download_files(self, dir_name):
        remote_path = "/home/shared/DATA/ENM-HWInventory"
        pattern = "'*.zip'"

        # Need to create a full remote path of every file in order to download otherwise we get:
        # 'FileNotFound: No such file error'
        rawcommand = "find {remote_path} -name {pattern}"
        command = rawcommand.format(remote_path=remote_path, pattern=pattern)

        if self.connect():
            stdin, stdout, stderr = self.client.exec_command(command, get_pty=True)
            file_list = stdout.read().splitlines()

            sftp = self.client.open_sftp()
            for file in file_list:
                file = file.decode("utf-8")
                (head, filename) = os.path.split(file)
                sftp.get(file, os.path.join('./', str(dir_name), filename))

            sftp.close()
            self.client.close()

    def extract_zip(self, folder):
        for (root, dirs, files) in os.walk(folder):
            for file in files:
                if file.endswith('.zip'):
                    print(f'Unzipping --> {file}')
                    # Create a ZipFile Object and load sample.zip in it
                    with ZipFile(os.path.join(folder, file), 'r') as zipObj:
                        # Extract all the contents of zip file in current directory
                        zipObj.extractall(folder)

    def create_csv(self, folder):
        for (root, dirs, files) in os.walk(folder):
            for file in files:
                if file.endswith('.xml'):
                    xml_parser(os.path.join(folder, file))
