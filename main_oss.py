import os
from modules import huawei_oss as oss

ftp_server = "ftpserver_ip"
username = "ftpuser"
passwd = "password"
ftp_directory = "/path/to/ftp/folder"

oss.get_xmls(username, passwd, ftp_server, ftp_directory)

cwd = os.getcwd()
for file in os.listdir(cwd):
    if file.endswith(".xml"):
        print("Generating CSV from {}".format(file))
        oss.xml_attributes(file)
