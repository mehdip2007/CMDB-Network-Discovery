from modules import ftp_ericsson
from modules import extract_and_csv
import os

hostname = "enm1.mtnirancell.ir"
user = "user"
passwd = "pass"
port = port

ftp = ftp_ericsson.Ssh(host=hostname, username=user, password=passwd, port=port, timeout=10)
ftp.download_files()

cwd = os.getcwd()
extract_and_csv.unzip(cwd)
extract_and_csv.xml_to_csv(cwd)
