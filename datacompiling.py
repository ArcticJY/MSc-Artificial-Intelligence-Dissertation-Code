import os
import pandas as pd

rootdir = "F:/KCLMastersFinalDissertation/loki_data/"
rootdir3d = "F:/KCLMastersFinalDissertation/csv_files/3d_labels/"
rootdircont = "F:/KCLMastersFinalDissertation/csv_files/contextual_labels/"

df_3d = pd.DataFrame()
df_2d = pd.DataFrame()
for subdir, dirs, files in os.walk(rootdir):
    for filename in os.listdir(subdir):
        if filename.endswith(".txt") and filename.startswith("label3d_"): 
            print(filename + " 3d labels")
            df_3d_temp = pd.read_csv((subdir + "/" + filename), sep=",")
            df_3d_temp['scenario'] = subdir.removeprefix("F:/KCLMastersFinalDissertation/loki_data/")
            df_3d_temp['frame'] = filename.removeprefix("label3d_").removesuffix(".txt")
            frames_3d = [df_3d, df_3d_temp]
            df_3d = pd.concat(frames_3d)

        elif filename.endswith(".json") and filename.startswith("label2d_"): 
            print(filename + " 2d contextual labels")
            df_2d_temp = pd.read_json((subdir + "/" + filename))
            df_2d_temp['scenario'] = subdir.removeprefix("F:/KCLMastersFinalDissertation/loki_data/")
            df_2d_temp['frame'] = filename.removeprefix("label2d_").removesuffix(".json")
            frames_2d = [df_2d, df_2d_temp]
            df_2d = pd.concat(frames_2d)

        else:
            continue

df_3d.to_csv(rootdir3d + "3d_labels.csv", sep=',', index=False, encoding='utf-8')        
df_2d.to_csv(rootdircont + "contextual_labels.csv", sep=',', index=True, encoding='utf-8')