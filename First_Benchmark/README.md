## First Benchmark
As explained in the Introduction Doc, we would like to cluster histopathological images of tumors from mice in order to try to split them into groups indicating their genome traits (i.e. having a specific genome snippet).

### The Process
Our process for the first benchmark is a very naive approach using regular image processing tools (QuPath) and K-means.
QuPath is a pathology software used by pathologists to diagnose pathological images. We used a few scripts made by people in Prof. Tzarfati’s Lab for the first steps:
1. __Split the images into smaller pieces:__
A histopathological image is in a very high resolution and is very big in size (can reach up to 6 GB per image). In order to overcome this, Prof. Tzarfati’s lab has created a script that tiles the huge image into 2000x2000 pixel images (about 10 MB). Out of the tiled image, we chose and saved 15 random tiles, which by Prof. Tzarfati’s estimation is about the number of tiles to approximately portray the image.
 ![image](https://user-images.githubusercontent.com/23155874/84882257-a8fe2680-b097-11ea-813c-1792434eab61.png)
![image](https://user-images.githubusercontent.com/23155874/84882360-ccc16c80-b097-11ea-8a30-b2fc76011b47.png)

2. __Identify and extract the nuclei from the image:__
Another script the lab has created is a script that uses regular image processing tools in order to segment nuclei an image and extract details per nuclei such as x,y of the nucleus center, nucleus radius, and more. All in all, there are about 1400 features extracted, not all of which are important.
![image](https://user-images.githubusercontent.com/23155874/84882400-dfd43c80-b097-11ea-8e04-0d7d96c9b406.png)

3. __Averaging the nuclei details per tiled image.__
4. __K-Means:__
	We thought of doing PCA as well but 1400 features are no problem for k-means.
![image](https://user-images.githubusercontent.com/23155874/84882461-f67a9380-b097-11ea-9c3b-92c21bca270c.png)

5. __Get the QTL analysis results:__ As described in the introduction doc, QTL analysis will allow us to estimate how good our clustering is. 
Another way for us to examine the clustering at this point would be to test the similarity of clusters of images that are tiled from the same scan.
From our results, it can be easily seen that images from the same scan are largely clustered the same.

### Known gaps in the above process
We know the above process has a lot (!) of gaps in it, but this is a first benchmark - the most naive thing we could do in order to get a metric for the data. Some of the gaps are:
* The geometrical representation of the data in the feature space extracted by the process may not be optimal for K-means algorithm.
* Only 15 images are taken into consideration per scan.
* They are taken at random.
* Averaging the features losses a lot of important information such as the number of nuclei per image, their formation, their closeness to each other, the size of the extremes (biggest and smallest) and much more
* The location of the tiled image in the original scan was not taken into account.
* No normalization of the image.


