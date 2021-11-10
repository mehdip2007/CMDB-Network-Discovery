import os
from modules import huawei_oss as oss

ftp_server = '10.130.200.133'
username = "ftpuser"
passwd = "Changeme_123"
ftp_directory = "/opt/oss/server/var/fileint/cm/InvtTimerExport"

oss.get_xmls(username, passwd, ftp_server, ftp_directory)

cwd = os.getcwd()
for file in os.listdir(cwd):
    if file.endswith(".xml"):
        print("Generating CSV from {}".format(file))
        oss.xml_attributes(file)
