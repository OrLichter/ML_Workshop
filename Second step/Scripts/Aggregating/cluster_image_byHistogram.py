import pandas as pd
import sklearn.cluster as cluster


dir_path = ##Complete the working directory


##K means for image clustering from nuclei clustering

cnt = 0
numFiles=81##################################################################
for i in range(2, 11):
    df = pd.read_csv(dir_path + "\\histogram2\\perK\\K="+str(i)+"\\histogram_preFile.csv")
    new_df = pd.DataFrame(df.loc[:, 'Image'])
    numpy = df.to_numpy()[:,1:(i+1)]
    dict = {"inertia": [], "nIters": []}

    for k in range(2, 11):###################################################3
        cnt += 1
        percentage = 100 * cnt // numFiles
        if (percentage % 2 == 0):
            print(percentage)
        kmeans = cluster.KMeans(n_clusters=k, max_iter=1000, tol=0.000001)
        kmeans.fit(numpy)
        #print(kmeans.labels_)

        new_df.insert(1, "K="+str(k), kmeans.labels_, allow_duplicates=False)
        #print(df.loc[:, ['label', 'Image']])
        dict["inertia"].append(kmeans.inertia_*(1/len(kmeans.labels_)))
        dict["nIters"].append(kmeans.n_iter_)
    dict_pd = pd.DataFrame.from_dict(dict, orient='index', columns=["K="+str(i) for i in range(2,11)])######################################3

    new_df.to_csv(dir_path + "\\histogram2\\perK\\K="+str(i)+"\\ImageClusters.csv")
    dict_pd.to_csv(dir_path + "\\histogram2\\perK\\K="+str(i)+"\\ImageClusters_InertiaAndNumIters.csv")

#new_df.to_csv("")
#print(new_df)