import sys, getopt, csv, time, os.path

import numpy as np

from sklearn import metrics
from sklearn.preprocessing import StandardScaler, normalize
from sklearn.cluster import MiniBatchKMeans, KMeans
from sklearn.metrics.pairwise import pairwise_distances_argmin

import matplotlib.pyplot as plt

def main():
	argv = sys.argv[1:]
	inputfile = ""
	clusters = 10

	# Get input file from command-line argument
	try:
	  opts, args = getopt.getopt(argv,"hi:c:",["ifile=", "num_clusters="])
	except getopt.GetoptError:
	  print 'test.py -i <inputfile> -c <num_clusters>'
	  sys.exit(2)

	for opt, arg in opts:
		if opt == '-h':
			print "dbscan.py -i <inputfile>"
			sys.exit(2)
		elif opt in ("-i", "--ifile"):
			inputfile = arg
			if not os.path.isfile(inputfile):
				print "File does not exist"
				sys.exit(2)
		elif opt in ('-c', '--num_clusters'):
			clusters = int(arg)

	kmeans(inputfile, clusters)

#Results currently only written when clustering on k=2
def write_results(labels, num_clusters):
	if num_clusters is not 2:
		return

	print "Getting anomalies for results"
	anom_label = 1
	label0 = np.count_nonzero(labels)
	if label0 < len(labels)/2:
		anom_label = 0

	results = ["Kmeans 2 Anomalies - ", label0]

	with open('kmeans_results.csv', 'a') as resultfile:
		writer = csv.writer(resultfile, delimiter=',', quotechar='"')
		writer.writerow(results)

	return


#num_clusters is the k value for kmeans clustering
def kmeans(inputfile, num_clusters):
	points = []
	labels_true = []
	with open(inputfile, 'rb') as datafile:
		reader = csv.reader(datafile, delimiter=',', quotechar='"')

		print 'Started adding points'
		for counter,point in enumerate(reader):
			float_point = map(float, point)
			points.append(float_point)
			labels_true.append(None)

	#Normalize the samples
	points = normalize(points)

	#Standardize the points - MAY NOT WORK WITH DISTRIBUTION OF DATA!
	# -removes mean
	# - scales to unit variance
	print 'Fit points to standarscaler'
	points = StandardScaler().fit_transform(points)

	#Cluster and get values for labels, cluster_centers, etc
	n_clusters = num_clusters
	k_means = KMeans(init='k-means++', n_clusters=num_clusters)
	k_means.fit(points)
	k_means_labels = k_means.labels_
	k_means_cluster_centers = k_means.cluster_centers_
	k_means_labels_unique = np.unique(k_means_labels)

	write_results(k_means_labels, num_clusters)


	# KMeans Graph Creation
	colors = plt.cm.Spectral(np.linspace(0, 1, num_clusters))
	for k, col in zip(range(n_clusters), colors):
	    my_members = k_means_labels == k
	    cluster_center = k_means_cluster_centers[k]
	    plt.plot(points[my_members, 0], points[my_members, 1], 'w',
	            markerfacecolor=col, marker='.')
	    plt.plot(cluster_center[0], cluster_center[1], 'o', markerfacecolor=col,
	            markeredgecolor='k', markersize=6)
	plt.title('KMeans')

	plt.show()


if __name__ == "__main__":
	main()