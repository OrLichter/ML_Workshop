import os
import pandas as pd
import sklearn.metrics as metrics

dir = ##complete working directory

#multi index
tuples=[]
metric = ["NMI", "AMI", "ARI", "HOMOGENEITY", "COMPLETENESS", "V_MEASURE", "FOWLKES_MALLOWS"]
for file in os.listdir(dir):
    lst = list(zip([file.split('.')[0]]*len(metric),metric))
    tuples = tuples + lst

index = pd.MultiIndex.from_tuples(tuples, names=['clustering_method', 'metric'])
#print(index)

columns = ["K="+str(i) for i in range(2,11)]
final_df = pd.DataFrame(index=index, columns=columns)
print(final_df)


##Extract GT

file_lookup = "Amet.csv" ##File containing all scans and data about each scan's mouse and line.
file = dir+"\\majority.csv"
df_scans = pd.read_csv(file)["Image"]
lookup = pd.read_csv(file_lookup)
lookup = lookup.loc[:,['Scan ', 'CC-Line']]
df_scans = pd.merge(df_scans, lookup, how = "left", left_on="Image", right_on="Scan ")
lines = lookup["CC-Line"].unique()
dict = {lines[i]:i for i in range(len(lines))}
dict_pd = pd.DataFrame.from_dict(dict, orient='index', columns=["GT"])
dict_pd = pd.merge(df_scans, dict_pd, how = "left", left_on="CC-Line", right_index=True)

#gt = [dict[line] for line in df_scans['CC-Line']]


for file in os.listdir(dir):
    print(file)
    full_file_path = dir + "\\" + file
    df = pd.read_csv(full_file_path)
    for i in range(2,11):
        k = "K="+str(i)
        print(k)
        cluster = df.loc[:,['Image', k]]
        #print(cluster)
        merged_cluster = pd.merge(dict_pd, cluster, how="left", left_on="Image", right_on="Image").rename(columns = {k:'cluster'})
        gt_array = merged_cluster["GT"].to_numpy()
        cluster_array = merged_cluster["cluster"].to_numpy()

        nmi = metrics.normalized_mutual_info_score(gt_array, cluster_array)
        final_df.loc[(file.split('.')[0], "NMI"), k] = nmi
        #print(final_df)

        ami = metrics.adjusted_mutual_info_score(gt_array, cluster_array)
        final_df.loc[(file.split('.')[0], "AMI"), k] = ami
        #print(final_df)

        ari = metrics.adjusted_rand_score(gt_array, cluster_array)
        final_df.loc[(file.split('.')[0], "ARI"), k] = ari
        #print(final_df)

        homogeneity_completeness_v_measure = metrics.homogeneity_completeness_v_measure(gt_array, cluster_array)

        homogeneity = homogeneity_completeness_v_measure[0]
        final_df.loc[(file.split('.')[0], "HOMOGENEITY"), k] = homogeneity
        #print(final_df)

        completeness = homogeneity_completeness_v_measure[1]
        final_df.loc[(file.split('.')[0], "COMPLETENESS"), k] = completeness
        #print(final_df)

        v_measure = homogeneity_completeness_v_measure[2]
        final_df.loc[(file.split('.')[0], "V_MEASURE"), k] = v_measure
        #print(final_df)

        fowlkes_mallows = metrics.fowlkes_mallows_score(gt_array, cluster_array)
        final_df.loc[(file.split('.')[0], "FOWLKES_MALLOWS"), k] = fowlkes_mallows
        print(final_df)

final_df.to_csv(dir + "\\metrics.csv")
