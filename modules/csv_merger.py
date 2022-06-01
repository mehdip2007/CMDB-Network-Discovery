from modules.init_packages import os
from modules.init_packages import glob
from modules.init_packages import pandas as pd


def merge(path, cisco_type):
    all_version_files = glob.glob(os.path.join(path, f"{cisco_type}/*.csv"))
    df_from_each_file = (
        pd.read_csv(f) for f in all_version_files if os.stat(f).st_size != 0
    )
    if df_from_each_file:
        concatenated_df = pd.concat(df_from_each_file, ignore_index=True)
        concatenated_df.to_csv(f"{path}_{cisco_type}_all.csv", index=False)
    else:
        with open(f"{path}_{cisco_type}_all.csv", 'w') as empty_csv:
            pass
    os.system(f"sed -i  '/,800MHz,/d' {path}_{cisco_type}_all.csv")