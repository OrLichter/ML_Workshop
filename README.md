# ML_Workshop – Breast Cancer Pathology Project
**Ron Tsibulsky**

**Or Lichter** 


## General Background:
In Professor Ilan Tzarfati’s lab, mice were split into groups, each group having specific genetic sequences that are suspected to be related to breast cancer development, and then breed. A group of offspring with the same genetic sequence (identified in their ancestors) is called a line. Tissue from the offspring was taken, stained in H&E, and classified by two professional pathologists as different types of breast cancer. Each image of the tumor is about 1.5 GB in size.

An example of a histopathologic image from google:
![image](https://user-images.githubusercontent.com/23155874/94159246-fd315780-fe8b-11ea-84f5-ffaee3008692.png)

 
## Goal:
Given pathological images of the tumors our goal is to divide the mice into groups by clustering (each mouse might have a few tissue images) and then divide each line into clusters as well.
 
## Key Metrics:
QTL (Quantitative Trait Locus) Analysis – is a statistical method that links two types of information—phenotypic data (trait measurements) and genotypic data (usually molecular markers)—in an attempt to explain the genetic basis of variation in complex traits. We will use QTL analysis to measure the line clustering.
Kaplan-Meier estimate - a non-parametric statistic used to estimate the survival function from lifetime data. We will use this metric to measure the individual mouse clustering.
Pathologist Classification - Compare our clustering to the pathologists’ classification of the data. 
(!) Ilan wants this to be a clustering problem and not a classification problem in order to examine the possibility to extract non-visible features from the images. Also, sometimes pathologists classify images differently as this is a subjective classification.
 
### A deeper dive into QTL and how we would use it:
QTL is a statistical method used to identify DNA snippets that are correlated with genetic traits (skin color, leaf size etc..). Ilan and his lab identified a few such snippets that might be correlated with the התפרצות of breast cancer. The lines were breed in order to have some of these snippets. The goal of this project is to see if we can group these lines in a way that the QTL graph (the output is a graph) shows significant differences for the DNA snippets.
