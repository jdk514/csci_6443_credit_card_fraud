#Identifying Potential Fraud in CC Data

##Purpose
This project is intended to create a method of identifying potential fraud. Our approach uses cluster methods to help identify atypical purchases. By identifying these purchases and determining their distance from a cluster we hope to be able to provide insight into the nature of the charges.


###Data Parser
To effectively use a number of clustering algorithms it is necessary to convert textual information into integer/float values.

For Example:
> Male => 1

> Female => 2

###DBSCAN
The first clusting algorithm used is dbscan. The file `dbscan.py` provides this functionality.