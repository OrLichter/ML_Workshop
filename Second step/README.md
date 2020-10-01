# Second Step

After getting familiar with the data, the process and having some ground results, we are diving deeper and trying some more advanced steps.
In this step we decided to cluster each __nuclei__ and not just each image. In order to do this we had to handle large amounts of data (such that couldn't fit into RAM at once).
So what did we do:

## Data Size
In the first step we explained about Qupath - the pathology tool that uses classical image analysis tools in order to extract features (around 1400) for each nuclei.
So for each nuclei we have 1,400 parameters, in an image there are about 6-10 thousand nuclei (for rough calculations, let's say 8). We have about 45 images per slide and 70 slides.
All in all 45*70*8000 = 25,200,000 nuclei so our data set is 25M X 1400 which definetly can't fit all into memory.

## MiniBatch Kmeans
