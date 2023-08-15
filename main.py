import pandas as pd

rootdir = "F:/KCLMastersFinalDissertation/loki_data/"
d_dir = "F:/KCLMastersFinalDissertation/csv_files/3d_labels/3d_labels.csv"
f_dir = "F:/KCLMastersFinalDissertation/csv_files/contextual_labels/contextual_labels.csv"
df_3d = pd.read_csv((d_dir), sep=",")
df_contextual = pd.read_csv((f_dir), sep=",")
df_pc = pd.DataFrame()

distance_thres = 10

scenarios = df_3d['scenario'].unique()

values = ['Car', 'Pedestrian']
df_3d = df_3d[df_3d.labels.isin(values) == True]
for i in scenarios:
    sc_df = df_3d.loc[df_3d['scenario'] == i]
    car_df = sc_df.loc[sc_df['labels'].isin(['Car', 'Bus', 'Truck', 'Van'])]
    print(car_df[' vehicle_state'])
    car_df = car_df.reset_index(drop=False)
    ped_df = sc_df.loc[sc_df['labels'] == 'Pedestrian']
    ped_df = ped_df.reset_index(drop=True)
    ped_x = ped_df[' pos_x'].values.astype(int)
    ped_y = ped_df[' pos_y'].values.astype(int)
    frames = sc_df['frame'].unique()
    for j in frames:
        current = car_df.loc[car_df['frame'] == j]
        uni_cars = current[' track_id'].unique()
        for k in uni_cars:
            selected = current.loc[current[' track_id'] == k] 
            x = selected[' pos_x'].values.astype(int)
            y = selected[' pos_y'].values.astype(int)
            for b in range(len(ped_x)):
                ped_ran = range(ped_df.loc[b, 'frame']-5, ped_df.loc[b, 'frame']+5)
                try:
                    distance = (int(x)-int(ped_x[b]))**2 + (int(y)-int(ped_y[y]))**2
                except:
                    print("Error Raised, Continuing...")
                    pass
                else:
                    distance = (int(x)-int(ped_x[b]))**2 + (int(y)-int(ped_y[y]))**2
                try:
                    ((car_df.loc[j, 'frame']) in ped_ran) and distance < 5
                except:
                    print("Error Raised, Continuing...")
                    pass
                else:
                    if ((car_df.loc[j, 'frame']) in ped_ran) and distance < 10 and (car_df.loc[j, 'frame']) < (ped_df.loc[b, 'frame']) and car_df.loc[j, 'scenario'] == ped_df.loc[b, 'scenario']:
                        print('possible collision')
                        try: 
                            print('car current actions: ' + str(car_df.loc[j, ' vehicle_state']))
                            print('car previous action: ' + str(car_df.loc[j-1, ' vehicle_state']))                               
                            currentintention = (car_df.loc[j, ' vehicle_state'])
                            previousintentions = {car_df.loc[j-1, ' vehicle_state'], car_df.loc[j-2, ' vehicle_state'], car_df.loc[j-3, ' vehicle_state'], car_df.loc[j-4, ' vehicle_state']}
                        except:
                            currentintention = (car_df.loc[j, ' vehicle_state'])
                            previousintention = (car_df.loc[j, ' vehicle_state'])
                            print(car_df.loc[j])
                            if previousintention == "Stopped" and currentintention != "Stopped":
                                entry = car_df.loc[[j]]
                                entry["Intention_Change"] = ["Negative"]
                                df_pc = pd.concat([df_pc,entry])
                            elif currentintention == "Stopped" and previousintention != "Stopped":
                                entry = car_df.loc[[j]]
                                entry["Intention_Change"] = ["Positive"]
                                df_pc = pd.concat([df_pc,entry])
                            else:
                                entry = car_df.loc[[j]]
                                entry["Intention_Change"] = ["Neutral"]
                                df_pc = pd.concat([df_pc,entry])
                            entry2 = ped_df.loc[[b]]
                            df_pc = pd.concat([df_pc,entry2])
                            print(entry2)
                        else:
                            currentintention = (car_df.loc[j, ' vehicle_state'])
                            previousintention = (car_df.loc[j-1, ' vehicle_state'])
                            print(car_df.loc[j])
                            if previousintention == "Stopped" and currentintention != "Stopped":
                                entry = car_df.loc[[j]]
                                entry["Intention_Change"] = ["Negative"]
                                df_pc = pd.concat([df_pc,entry])
                            elif currentintention == "Stopped" and previousintention != "Stopped":
                                entry = car_df.loc[[j]]
                                entry["Intention_Change"] = ["Positive"]
                                df_pc = pd.concat([df_pc,entry])
                            else:
                                entry = car_df.loc[[j]]
                                entry["Intention_Change"] = ["Neutral"]
                                df_pc = pd.concat([df_pc,entry])
                            entry2 = ped_df.loc[[b]]
                            df_pc = pd.concat([df_pc,entry2])
                            print(entry2)
                    else:   
                        continue
    df_pc.to_csv(rootdir + "possible_collisions.csv", sep=',', index=False, encoding='utf-8')

