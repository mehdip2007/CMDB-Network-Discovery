import pandas as pd
import glob
import os


path = r'/Users/mehdi/Ariana/Cisco/1/cisco/cisco_ipbb/version'

all_files = glob.glob(os.path.join(path, "*.csv"))
df_from_each_file = (pd.read_csv(f) for f in all_files)
concatenated_df = pd.concat(df_from_each_file, ignore_index=True)

concatenated_df.to_csv('/Users/mehdi/Ariana/Cisco/1/cisco/cisco_ipbb/cisco_ipbb_version.csv', index=False)

