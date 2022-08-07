from dotenv import dotenv_values
from csv_reader_update_create_insight import reader
import sftp_class
import os
import shutil
import logging

logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.DEBUG,
                    filename='ENM.log', filemode='w')

logger = logging.getLogger()
cwd = os.path.dirname(os.path.abspath(__file__))
csv_files_dir = os.path.join(cwd, "csv_files")
config = dotenv_values("../.env")

hostnames = ["enm1.mtnirancell.ir", "enm2.mtnirancell.ir", "enm3.mtnirancell.ir"]
port = 5022

os.makedirs(csv_files_dir, exist_ok=True)

for hostname in hostnames:
    logger.info(f"Getting Data from {hostname}...")
    dir_name = hostname.split('.')[0]
    os.makedirs(dir_name, exist_ok=True)
    sftp = sftp_class.Sftp(host=hostname, username=config.get("ericsson_username"),
                           password=config.get("ericsson_password"), port=port, timeout=10)

    sftp_files_path = os.path.join(cwd, dir_name)
    sftp.download_files(sftp_files_path)
    logger.info(f"***Download Finished for {hostname}.")
    sftp.extract_zip(sftp_files_path)
    sftp.create_csv(sftp_files_path)

    logger.info(f"Moving File {sftp_files_path}...")
    file_names = os.listdir(sftp_files_path)
    for file_name in file_names:
        if file_name.endswith(".csv"):
            shutil.copy(os.path.join(sftp_files_path, file_name), csv_files_dir)
            logger.info(f"File Copied to {file_name} Successfully")

csvs = os.listdir(csv_files_dir)
for csv in csvs:
    logger.info(f"reading csv file {csv}.. ")
    reader(os.path.join(csv_files_dir, csv))
