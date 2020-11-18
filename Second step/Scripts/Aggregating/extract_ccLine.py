import pandas as pd

dirS =r"C:\Users\ront\Desktop\Kmeans\Kmeans Mini Batch (Standard Scaler)\Image_Kmeans_allTables\\"
dirM=r"C:\Users\ront\Desktop\Kmeans\Kmean Mini Batch (MinMax Scaler)\Image_Kmeans_allTables\\"
dirs = [dirS, dirS]
files = ["standard_scaler_meanNuclei_cluster.csv", "standard_scaler_meanNuclei_cluster.csv"]
Ks = ["K=4", "K=3"]
#file_kMeansResults = r"C:\Users\ront\Desktop\Kmeans\Kmean Mini Batch (MinMax Scaler)\Image_Kmeans_allTables\histogram_K=7.csv"
#file_kMeansResults = r"C:\Users\ront\Desktop\Kmeans\Kmeans Mini Batch (Standard Scaler)\Image_Kmeans_allTables\histogram_K=10.csv"
#k_chosen = "K=10"
file_lookup = "Amet.csv"

assert (len(dirs) == len(files) and len(files)==len(Ks))
for i in range(len(dirs)):
    file = dirs[i] + files[i]
    df = pd.read_csv(file)
    lookup = pd.read_csv(file_lookup)
    lookup = lookup.loc[:,['Scan ', 'CC-Line']]

    #lookup = lookup[['Scan', 'CC-Line']]
    df['Image'] = df['Image'].apply(lambda x: x.replace('_', '.').split('.')[0])
    print("shape of original dataframe:")
    print(df.shape)
    merged = pd.merge(df, lookup, how = "left", left_on="Image", right_on="Scan ")
    merged.to_csv("merged_Amet.txt", sep = ' ', index = None)
    print("shape of merged dataframe:")
    print(merged.shape)

    line_dict = {"4052" : "IL-4052" , "L4052" : "IL-4052", "L72" : "IL-72", "L4457" : "IL-4457" , "L111" : "IL-111" , "L188" : "IL-188" , "L1912" : "IL-1912" ,
                 "L3912" : "IL-3912" , "L557" : "IL-557" , "L3348" : "IL-3348" , "L519" : "IL-519"}


    def correct_line(line):
        return line_dict[line]


    part_df = (merged.loc[:,[Ks[i], 'CC-Line']])
    part_df["CC-Line"]= part_df["CC-Line"].apply(correct_line)
    part_df=part_df.groupby(by=["CC-Line", Ks[i]]).size().reset_index(name='counts')
    final_df = (part_df.pivot_table(values='counts', index="CC-Line", columns=Ks[i], aggfunc='first').fillna(0))
    final_df.insert(loc=0, column='CC.Line', value=final_df.index)
    final_df = (final_df.rename(columns = {0:'A', 1:'B', 2:'C', 3:'D', 4:'E', 5:'F', 6:'G', 7:'H', 8:"I", 9:"J", Ks[i]:'CC.Line'}).iloc[:,0:])
    print(final_df)

    final_df = (final_df.set_index('CC.Line'))
    final_df.to_csv(dirs[i]+files[i]+"_"+Ks[i]+".csv")
    final_df.to_csv(dirs[i]+files[i]+"_"+Ks[i]+".txt", sep="\t")
#final_df.to_csv(r"C:\Users\ront\Desktop\Kmeans\Kmeans Mini Batch (Standard Scaler)\Image_Kmeans_allTables\test.csv")





'''
for i in range(10):
    to_save = merged.loc[:,['CC-Line', str(i+1)]]
    to_save.to_csv("p53_forQTL_K="+str(i+1)+".txt", sep = ' ', index=None)
'''