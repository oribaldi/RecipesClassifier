################################################################
#
# TUM Machine Learning 
# Final Project : Recipes Classification
# 
# Author: Oriana Baldizan
# Data:   February 2015
#
# clustering.py : defines the Clustering class
#
# Performs a clustering technique to cluster a list of recipes
# Techniques: k-means and hierarchical clustering
#
# Observations:
# This k-means version initializes the means as follows:
# 1. Picks a random point
# 2. Succesively picks other k-1 points, as farthest from the
#    previous ones
#
################################################################

# Python Modules
import math
import random as rand
from collections import defaultdict

# K-dtree Library Modules
import kdtree

class Clustering:
	""" Clustering Algorithm """

	def __init__(self, points):

		self.k        = 2
		self.means    = []
		self.points   = points
		self.clusters = defaultdict(list)


	def _next_further_point(self, points, centroids):
		""" Returns furthest point from centroids """

		tree = kdtree.create(centroids)
		#dic  = {}
		
		further_point = (points[0], 0) # To always have the further point
		for point in points:

			# Get distance to all centroids
			#dic[point] = 0
			dist = 0
			for node in list(tree.inorder()):
				#dic[point] += node.dist(point)
				dist += node.dist(point)

			# Check if we found a better point
			if further_point[1] < dist:
				further_point = (point, dist)

		return further_point[0]


	def _initial_means(self):
		""" Initialize each cluster mean (centroid) """

		points    = self.points[:]
		clusters  = defaultdict(list)
		centroids = []

		# Pick a random point
		p = rand.choice(points)
		points.remove(p)
		clusters[0].append(p)
		centroids.append(p)

		# Pick k-1 points as farthest as previous
		for i in range(1, self.k):
			p = self._next_further_point(points, centroids)
			points.remove(p)
			clusters[i].append(p)
			centroids.append(p)

		return centroids


	def _assign_points(self):
		""" Assign points to the closest cluster """

		tree     = kdtree.create(self.means[:])
		clusters = defaultdict(list)

		# print "Assign to closest cluster "

		for point in self.points:
			
			closest_centroid = (tree.data, 1000)
			for node in list(tree.inorder()):

				# print "Distance from point " + str(point) + " to center " + str(node.data)
				
				dist = node.dist(point)
				if dist <= closest_centroid[1]:
					closest_centroid = (node.data, dist)
				# elif dist == closest_centroid[1]:
				# 	closest_centroid = rand.choice([closest_centroid, (node.data, dist)])

			# print "Point " + str(point) + " with centroid " + str(closest_centroid)
			# print ""

			# Update cluster
			clusters[closest_centroid[0]].append(point)

		return clusters


	def _calculate_mean(self, cluster):
		""" Calculate the mean point of the given cluster """

		# Sum all points by dimension (1,2) + (1,2) = (2,4)
		# and divide each dimension with the number of points in cluster
		mean = [float(sum(x) / float(len(cluster)) ) for x in zip(*cluster)]

		return tuple(mean)

	def _update_means(self, clusters):
		""" Update clusters' mean """

		# print clusters.values()

		new_means = []

		for cluster in clusters.values():
			# print cluster
			new_mean = self._calculate_mean(cluster)
			new_means.append(new_mean)

		# for centroid in self.means:
		# 	for cluster in clusters[centroid]:
		# 		new_mean = self._calculate_mean(cluster)
		# 		new_means.append(new_mean)

		return new_means


	def _convergence_reached(self, means, threshold):
		""" Checks if convergence has been reached """

		# print "New means " + str(means)
		# print "Old means " + str(self.means)

		for i in range(0,len(self.means)):
			new_mean = means[i]
			old_mean = self.means[i]

			# print "New mean " + str(new_mean)
			# print "Old mean " + str(old_mean)

			# Caldulate the difference
			s  = [math.pow(x-y,2.0) for x,y in zip(new_mean, old_mean)]
			sr = math.sqrt( sum(s) )

			# print "Difference " + str(sr)

			if sr > threshold:
				return False

		return True


	def _is_member(self, point, mean):
		""" Returns 1 if point is in cluster of mean, 0 otherwise """

		for p in self.clusters[mean]:
			if p == point:
				return 1

		return 0


	def objective_function(self):
		""" Returns the value of k-means objective function J """

		J = 0

		for mean in self.clusters.keys():
			for point in self.points:
				i = self._is_member(point,mean)
				d = [math.pow(x-y,2.0) for x,y in zip(point, mean)]
				s = [i*x for x in d]
				J += sum(s)

		return J


	def kmeans(self, number_of_clusters):
		""" Implementation of k-means algorithm """

		self.k = number_of_clusters

		# Initialize means
		self.means = self._initial_means()
		clusters   = defaultdict(list)

		# print self.means
		# print " "

		# Continue until convergence
		converged = False
		while not converged:

			# Assign each point to the closest cluster
			clusters = defaultdict(list)
			clusters = self._assign_points()

			# print "Current clusters"
			# print clusters.values()
			# print " "

			# Update means
			means = []
			means = self._update_means(clusters)

			# print "Update means"
			# print means
			# print ""

			# # Check if we reached convergence
			converged = self._convergence_reached(means, 0.01)

			if not converged:
				self.means = []
				self.means = means[:]

			# print "Self means"
			# print self.means

		self.clusters = clusters

		return self.clusters

