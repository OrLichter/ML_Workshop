import pandas as pd
pd.set_option('display.max_rows', 1000)
import numpy as np
import sklearn.preprocessing as preprocessing
import sklearn.cluster as cluster
import matplotlib.pyplot as plt
file = "mean_images.csv"
df = pd.read_csv(file)
print("read file succesfully")
print("data frame shape: " + str(df.shape))
print (type(df['Image']))

numpy_obj = np.float64(df.to_numpy()[:,7:])
print("numpy object contains empty values: " + str(np.isnan(numpy_obj).any()))
print ("numpy shape: " + str(numpy_obj.shape))


scaler = preprocessing.StandardScaler()
scaler.fit(numpy_obj)
stand_numpy_obj = scaler.transform(numpy_obj)


new_df = pd.DataFrame(df.loc[:, 'Image'])
inertia=[]
n_iters=[]


for k in range(1, 11):
    print (k)
    kmeans = cluster.KMeans(n_clusters=k, max_iter=1000, tol=0.000001)
    kmeans.fit(stand_numpy_obj)
    #print(kmeans.labels_)

    new_df.insert(1, str(k), kmeans.labels_, allow_duplicates=False)
    #print(df.loc[:, ['label', 'Image']])
    inertia.append(kmeans.inertia_*(1/830))
    n_iters.append(kmeans.n_iter_)

new_df.to_csv("standarized_labels.csv")
#print(new_df)

fig, (ax1, ax2) = plt.subplots(2)
fig.suptitle('Results for standarized data')
ax1.plot(range(1,11), inertia)
ax1.set_title('Mean Inertia')
ax2.plot(range(1,11), n_iters)
ax2.set_title('num of Iterations to convergence')
plt.savefig("standarization_graphs")

print(inertia)
plt.show()



