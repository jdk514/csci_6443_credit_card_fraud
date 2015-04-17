import csv, pdb
import ddbscan
#I think that 5 is a good min cluster number as values come in clumps of 5
# Currently looking like 50
scan = ddbscan.DDBSCAN(50,5)

with open('min2_parsedfile.csv', 'rb') as datafile:
	reader = csv.reader(datafile, delimiter=',', quotechar='"')

	print 'Started adding points'
	for counter,point in enumerate(reader):
		float_point = map(float, point)
		scan.add_point(point=float_point, count=1, desc="")

	print 'Started computing'
	scan.compute()

	print 'Clusters found and its members points index:'
	cluster_number=0
	for cluster in scan.clusters:
		print '=== Cluster %d ===' % cluster_number
		print 'Cluster points index: %s' % list(cluster)
		cluster_number += 1

	anomaly_points = 0
	print '\nCluster assigned to each point:'
	for i in xrange(len(scan.points)):
		print '=== Point: %s ===' % scan.points[i]
		print 'Cluster: %2d' %scan.points_data[i].cluster
		# -1 point cluster is anonmoly - potential fraud!!
		if scan.points_data[i].cluster == -1:
			print '\t <=== Anomaly found!'
			anomaly_points += 1
		else:
			print

	print 'Anomalies found %d outside %d clusters' % (anomaly_points, cluster_number)
