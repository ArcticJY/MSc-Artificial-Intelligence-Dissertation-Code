import os
import re
import string
import pandas as pd
import matplotlib as plt

dircorrellation = "F:/KCLMastersFinalDissertation/loki_data/possible_collisions.csv"
f_dir = "F:/KCLMastersFinalDissertation/csv_files/contextual_labels/contextual_labels.csv"
raw_df = pd.read_csv((dircorrellation), sep=",")
contextual_df = pd.read_csv((f_dir), sep=",")

ped_df = raw_df.loc[raw_df['labels'] == 'Pedestrian']
ped_df = ped_df.reset_index(drop=False)

car_df = raw_df.loc[raw_df['labels'] == 'Car']
car_df = car_df.reset_index(drop=False)

row_count = len(ped_df)

contextual_df = contextual_df.drop(columns=['Car', 'Bus', 'Truck', 'Van', 'Motorcyclist', 'Bicyclist', 'Wheelchair', 'Traffic_Sign', 'Traffic_Light', 'Potential_Destination', 'Road_Entrance_Exit'], axis=1)
contextual_df = contextual_df.dropna()
contextual_df = contextual_df.reset_index(drop=True)

g_attributes = []
a_attributes = []
for idx, row in contextual_df['Pedestrian'].items():
    r = contextual_df.loc[idx, 'Pedestrian']
    #a = re.search(r'\b(attributes)\b', r)
    translating = str.maketrans('', '', string.punctuation)
    b = r.translate(translating)
    blist = b.split(" ")
    if 'Male' in blist:
        g_attributes.append("Male")
        if 'Adult' in blist:
            a_attributes.append("Adult")
        else:
            a_attributes.append("Child")
    else:
        g_attributes.append("Female")
        if 'Adult' in blist:
            a_attributes.append("Adult")
        else:
            a_attributes.append("Child")

contextual_df.rename(columns={'Unnamed: 0':'track_id'}, inplace = True)
ped_df["Age"] = 'NaN'
ped_df["Gender"] = 'NaN'


for idx, row in ped_df[' track_id'].items():
    current_id = ped_df.loc[idx, ' track_id']
    index = contextual_df.index[contextual_df['track_id'] == current_id].tolist()
    if index:
        ped_df.loc[idx, 'Age'] = a_attributes[index[0]]
        ped_df.loc[idx, 'Gender'] = g_attributes[index[0]]
    index = []
     
result_df = ped_df.filter(['Age', 'Gender'], axis=1)
result_df['Intentions_Change'] = car_df.filter(['Intention_Change'], axis=1)
ax = ped_df.plot.bar()