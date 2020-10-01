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



/*******************
Rons Part
********************/

## Visualizing the Data
One of the features extracted from QuPath is the x,y pixel center for each nuclei. We though - we have the center pixels, we have a cluster for each nuclei, why not try to visualize it?! So that's what we did.
You can use the `ImageChange2NucleiClasses.py` to download the data saved in my Google Drive, or refer it to a local path and get the following image:
![image](https://user-images.githubusercontent.com/23155874/94807228-04aab080-03f8-11eb-8ff1-c75ac895cbf5.png)



