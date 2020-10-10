import os
import pandas as pd

import numpy as np

dir_path = ##Complete the working directory

###Create histogram

new_df = np.array([])
pds = []
numFiles = len(os.listdir(dir_path)) - 2
cnt = 0
for file in os.listdir(dir_path):
    if (file=='histogram' or file=='histogram2' or file=='majority.csv'):
        continue
    cnt += 1
    percentage = 100 * cnt // numFiles
    if (percentage % 2 == 0):
        print(percentage)
    new_df = pd.DataFrame(index=[0, 1, 2, 3, 4 ,5 ,6, 7, 8, 9])
    file_path = dir_path + "\\" + file
    df = pd.read_csv(file_path)
    df_nuclei_clusters=(df.iloc[:, 7:])
    #print(df_nuclei_clusters)
    for column in df_nuclei_clusters.iloc[:,2:].columns:
       # print(column)
        #print(type(column))
        dict = df_nuclei_clusters[column].value_counts(normalize=True).reindex([0, 1, 2, 3, 4, 5, 6, 7, 8, 9]).to_dict()
        new_df[column] = pd.Series(dict)
        #print(new_df)
    new_df.to_csv(dir_path + "\\histogram2\\" + file)



##conclude from histogram to one file per k

Ks = ["K="+str(i) for i in range(2,11)]
numFiles = (len(os.listdir(dir_path+"\\histogram2")) - 1)*9
cnt = 0
for k_string in Ks:
    os.mkdir(dir_path + "\\histogram2\\perK\\"+k_string)
    new_df = pd.DataFrame()
    for file in os.listdir(dir_path+"\\histogram2"):
        if (file == 'perK'):
            continue
        cnt += 1
        percentage = 100 * cnt // numFiles
        if (percentage % 2 == 0):
            print(percentage)
        file_path = dir_path + "\\histogram2\\" + file
        dict = pd.read_csv(file_path)[k_string].to_dict()
        Image = file.split('_')[0]
        dict['Image'] = file.replace('_', '.').split('.')[0]
        new_df = new_df.append(dict, ignore_index=True).fillna(0.0)
    new_df.to_csv(dir_path + "\\histogram2\\perK\\"+k_string + "\\histogram_preFile.csv")


