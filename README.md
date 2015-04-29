#Identifying Potential Fraud in CC Data

##Purpose
This project is intended to create a method of identifying potential fraud. Our approach uses cluster methods to help identify atypical purchases. By identifying these purchases and determining their distance from a cluster we hope to be able to provide insight into the nature of the charges.


###Data Parser
To effectively use a number of clustering algorithms it is necessary to convert textual information into integer/float values.

For Example:
> Male => 1

> Female => 2

run with `python data_parser.py` - requires that the original data file is in the location the program is run

###Binary Parser
Due to how distance between points is calculated, by evaluating fields like `sector` into integer values ('Auto' => 4, 'Travel' => 10) breaks down the relationship between points. Thus this parser creates a new field for every string value and equates the field to a boolean. The field will be *1* if the value exists in the record, but defaults to *0*. The expectation being that this will preserve the value added of each string, but not destroy relative location

run with `python binary_parser.py` - requires that the original data file is in the location the program is run

###DBSCAN
The first clusting algorithm used is dbscan. The file `dbscan.py` provides this functionality.

run with `python dbscan.py -i <inputfile>`

###Sklearn DBSCAN
This file `sklearn_dbscan.py` provides similar functionaliyt as `dbscan.py`, but also includes the following benefits:
 - Normalization of data
  - Ensures that each column is weighted equally
 - Transforms points through `StandardScaler()` to smooth data
 - Calcualtes statistics on NearestNeighbor of anomalies
 - Writes results to a csv file `dbscan_results.csv`
 - Creates a graphical representation of datapoints
  - Only works if there is a visual output

run with `python sklearn_dbscan.py -i <inputfile> -e <epsilon> -c <min_cluster_size>`

###Sklearn KMeans
`sklearn_kemans.py` will run the data against the KMeans algorithm, it provides the following features:
 - Nomralization of data
  - Ensures that each column is weighted equally
 - Transforms points through `StandardScaler()` to smooth data
 - Writes results to a csv file `kmeans_results.csv`, if k=2
  - This includes a list of anomalies

run with `python sklearn_kmeans.py -i <inputfile> -c <num_clusters>`