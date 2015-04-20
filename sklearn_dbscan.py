import sys, getopt, csv
import os.path
import numpy as np

from sklearn.cluster import DBSCAN
from sklearn import metrics
from sklearn.datasets.samples_generator import make_blobs
from sklearn.preprocessing import StandardScaler, normalize
from sklearn.neighbors import NearestNeighbors

import pdb

def main():
	argv = sys.argv[1:]
	inputfile = ""
	eps = 1
	min_samples = 5

	# Get input file from command-line argument
	try:
	  opts, args = getopt.getopt(argv,"hi:e:c:",["ifile=", "min_cluster=", "eps="])
	except getopt.GetoptError:
	  print 'test.py -i <inputfile>'
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
		elif opt in ('-e', '--eps'):
			eps = float(arg)
		elif opt in ('-c', '--min_cluster'):
			min_samples = float(arg)

	dbscan(inputfile, eps, min_samples)

def write_result(eps, min_samples, inputfile, clusters, anomalies, anom_mean, anom_std):
	with open('dbscan_results', 'a') as resultfile:
		writer = csv.writer(resultfile, delimiter=',', quotechar='"')
		writer.writerow([inputfile, eps, min_samples, clusters, anomalies, anom_mean, anom_std])

	return


def dbscan(inputfile, eps, min_samples):
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

	#Setup our dbscan functionality
	# - Distance is 50
	# - Min elements is 5
	print 'Fit points to DBSCAN'
	db = DBSCAN(eps=eps, min_samples=min_samples).fit(points)
	#unsure of functionality
	core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
	core_samples_mask[db.core_sample_indices_] = True
	labels = db.labels_

	#Determine the clusters in dataset
	print 'Count clusters'
	n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)

	print('Estimated number of clusters: %d' % n_clusters_)
	print("Homogeneity: %0.3f" % metrics.homogeneity_score(labels_true, labels))
	print("Completeness: %0.3f" % metrics.completeness_score(labels_true, labels))
	print("V-measure: %0.3f" % metrics.v_measure_score(labels_true, labels))
	print("Adjusted Rand Index: %0.3f"
	      % metrics.adjusted_rand_score(labels_true, labels))
	print("Adjusted Mutual Information: %0.3f"
	      % metrics.adjusted_mutual_info_score(labels_true, labels))
	#print("Silhouette Coefficient: %0.3f"
	#    % metrics.silhouette_score(points, labels))

	print 'Calculate Nearest Neighbor'
	#n_neighbors must equal 2, since n_neighbor=1 returns the given node rather than a neighbor
	f_nbr = NearestNeighbors(n_neighbors=2, algorithm="ball_tree").fit(points)
	distances, indices = f_nbr.kneighbors(points)

	anoms = 0
	anoms_dist = []
	total_anon_nbr_distance = 0
	for counter,point in enumerate(labels):
		if point == -1:
			anoms += 1
			anoms_dist.append(distances[counter][1])

	#Calculate the meand and standard deviation of the distance to nearest neighbors of anomalies
	anom_dist_arr = np.array(anoms_dist)
	anom_mean = np.mean(anoms_dist)
	anom_std = np.std(anoms_dist)

	print 'Anomalies are on average %f distance from nearest neighbor' % anom_mean
	print 'Anomalies distance has standard deviation of %f' % anom_std

	write_result(eps=eps, min_samples=min_samples, inputfile=inputfile, clusters=n_clusters_, anomalies=anoms, anom_mean=anom_mean, anom_std=anom_std)
	# avg_anom_dist = total_anon_nbr_distance / float(anoms)
	# print("Anomalies: %d with avg neighbor %f away") % (anoms, avg_anom_dist)

	import matplotlib.pyplot as plt

# Black removed and is used for noise instead.
	unique_labels = set(labels)
	colors = plt.cm.Spectral(np.linspace(0, 1, len(unique_labels)))
	for k, col in zip(unique_labels, colors):
	    if k == -1:
	        # Black used for noise.
	        col = 'k'

	    class_member_mask = (labels == k)

	    xy = points[class_member_mask & core_samples_mask]
	    plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=col,
	             markeredgecolor='k', markersize=14)

	    xy = points[class_member_mask & ~core_samples_mask]
	    plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=col,
	             markeredgecolor='k', markersize=6)

	plt.title('Estimated number of clusters: %d' % n_clusters_)
	plt.show()


if __name__ == "__main__":
	main()