import os
import pandas as pd


dir_path = ## The path where each image's nuclei clusters are saved.
'''
The Nuclei clusters should be saved in the following format:
For Each image there is a csv file, in which each row represents a nucleus, and the columns are as follows:
column 0: index
column 1: "Unnamed" - same values as index (Not really important)
column 2: 'Image" = contains image name, starting with the name of the scan
column 3: 'Name' (Not really important)
column 4: 'Class' (Not really important)
column 5: 'Parent' (Not really important)
column 6: 'ROI' (Not really important)
Column 7: 'Centroid X' (Not really important)
column 8: 'Centroid Y' (Not really important)

Following 9 columns are K= 2 to 10.
'''

new_df = pd.DataFrame()
numFiles = len(os.listdir(dir_path)) - 3
cnt = 0
for file in os.listdir(dir_path):
    if file=='histogram' or file=='histogram2' or file=='Image_Kmeans_allTables':
        continue
    cnt+=1
    percentage = 100*cnt//numFiles
    if (percentage%2==0):
        print(percentage)
    dict={}

    file_path = dir_path + "\\" + file
    df = pd.read_csv(file_path).iloc[:, 9:]
    Image = pd.read_csv(file_path)['Image'][0].replace('_', '.').split('.')[0]
    majority = df.mode(axis=0).iloc[0].to_dict()
    majority['Image'] = Image
    #print(type(majority.iloc[0]))
    #print("majority:")
    #print(majority)
    #print(majority)
    new_df = new_df.append(majority, ignore_index=True)
#print(new_df)
new_df.to_csv(dir_path + r"\majority.csv")


