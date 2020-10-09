# Second Step

After getting familiar with the data, the process and having some ground results, we are diving deeper and trying some more advanced steps.
In this step we decided to cluster each __nuclei__ and not just each image. In order to do this we had to handle large amounts of data (such that couldn't fit into RAM at once).
So what did we do:


## Data Size
In the first step we explained about Qupath - the pathology tool that uses classical image analysis tools in order to extract features (around 1400) for each nuclei.
So for each nuclei we have 1,400 parameters, in an image there are about 6-10 thousand nuclei (for rough calculations, let's say 8). We have about 45 images per slide and 70 slides.
All in all 45*70*8000 = 25,200,000 nuclei so our data set is 25M X 1400 which definetly can't fit all into memory.


## Scaling
One of the first steps in any ML algorithm is to scale the data. This makes the learning process a lot less susceptible to scale difference, for example if one feature is nuclei size which is in scale 10^-6 while another feature is nuclei blue color which is a number from 1-255, then a small difference in the hue of the nuclei might cause a big difference to the learning model.
Here we first meet our data size problem. Some scaling algorithms such as RobustScaler (which uses quantiles in order to remove outliers before normalizing to standard distribution) need to have the whole data in memory in order to work properly. Luckily some of the more simple and familiar scaling algorithms keep a few parameters that can be calculated over the data iteratively and do not need the whole dataset in memory. 
We have used [MinMax scaler](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.MinMaxScaler.html?highlight=minmax#sklearn.preprocessing.MinMaxScaler) and [standard scaler](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.StandardScaler.html).

### MinMax Scaler
From its name it's not too hard to uderstand what it does. This scaler goes over all data (`fit`), keeps in memory the maximum and minimum of each parameter. After going over all data it goes over all data again (`transform`) and transforms the data between 0 and 1. Specifically this is the formula for the calculation:
```
X_std = (X - X.min(axis=0)) / (X.max(axis=0) - X.min(axis=0))
X_scaled = X_std * (max - min) + min
```
You can find the trained scaler under `Pickled Data -> MinMax_scaler.pickle`

### Standard Scaler
This scaler takes each feature of the data and transforms it to be normally distributed. The process is still prety simple - over the first iteration of the data (`fit`) the scaler calculates the mean and the standard deviation. On the second run of the data (`transform`) it scales the data to be normally distributed:
```
z = (x - mean) / stdv
```
You can find the trained scaler under `Pickled Data -> standard_scaler.pickle`

## MiniBatch Kmeans
Most clustering algorithms need to have all the data in order to work. Kmeans, needs all the data in order to perform the iteration on centers and to calculate the distances, DBSCAN needs all data in order to count the number of data points in epsilon distance and so on... 
After some searching we found [MiniBatch Kmeans](https://scikit-learn.org/stable/modules/clustering.html#mini-batch-kmeans). The algorithm assumes we sample iid samples from the dataset and performs Kmeans on them while keeping the center average of all sampled data. Using this algorithm we managed to cluster the huge data.


## Aggregating the Data

After clustering the nuclei, we had to determin a clustering for each image.
In order to do so, we decided on three methodologies:
1)	**Majority Vote**:
Clustering each image with a "majority vote" of the image's nuclei clusters. 
For examples, if the nuclei are clustered in groups 0-4, and for an image most of the nuclei are clustered to group 3, then the entire image is clustered to group 3. 
Specifically, it means the number of possible clusters for images is the same as number of possible clusters for nuclei.
The code for this can be found in file `majority_vote`.

2)	**Histogram**:
Here we have calculated the percentage of nuclei of each cluster at each image. This way we have created for each image a k-dimensional vector , where k is the number of possible clusters for nuclei, so that feature i in this vector represents the percentage of nuclei (in that specific image) clustered to group i. On these k-dimensoinal vectors we have run another K-means process to cluster the images.
In this method the number of possible clusters for images does not depend on the number of possible clusters for nuclei. For example, on the nuclei level we can cluster to 7 groups, and on the image level to 4 groups only. 
We have ran all variations for number of nuclei clusters between 2 to 10, with number of image clusters between 2 to 10 (81 variations at all).

3) **Image average**:
We have clustered images "straight forward" (using K-means) without clustering nuclei before hand, by calculating an average on all nuclei for each image (The average was calculated feature-wise, so that if Qpath gave us for each nucleus an ~1400 dimensional vector of features, we calculate an ~1400 dimensional average vector for the entire image). 


## Metrics
Besides evaluating our clusters on QTL and Kaplan-Meir analyses, we have tested our results using some common clustering metrices. 
These metrices require ground-truth labeling, which we don't have, so we did the following, knowing that the results of these metrices should be taken with limited importance:

We have created a "ground-truth" labeling by looking at each mice line as a group, and clustering each image according to it's mouse's line. 
The metrices we have used are:
-	NMI (Normalized Mutual Information)
-	AMI (Adjusted Mutual Information)
-	ARI (Adjusted Rand Index)
-	Homogeneity
-	Completeness
-	V_Measure (Which calculates an average of the above two metrices)
-	Fowlkes Mallows

We are familiar also with metrices that do not require ground truth labels, such as Silhouette metric,  clustered objects. Nevertheless, as it is not clear what would be a right distance function between the clustered images, and as calculating the distance of such a large dataset is computationally hard we have decided not to calculate these metrics.



## Visualizing the Data
One of the features extracted from QuPath is the x,y pixel center for each nuclei. We though - we have the center pixels, we have a cluster for each nuclei, why not try to visualize it?! So that's what we did.
You can use the `ImageChange2NucleiClasses.py` to download the data saved in my Google Drive, or refer it to a local path and get the following image:
![image](https://user-images.githubusercontent.com/23155874/94807228-04aab080-03f8-11eb-8ff1-c75ac895cbf5.png)



## Process Flow

![Flowchart](https://user-images.githubusercontent.com/23155874/95594965-4a005b00-0a54-11eb-9787-be1cbee70d13.png)
