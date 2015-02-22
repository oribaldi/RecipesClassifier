#########################################################
#
# TUM Machine Learning 
# Final Project : Recipes Classification
# 
# Author: Oriana Baldizan
# Data:   February 2015
#
# recipe_recommender.py : defines the Recommender class
#
# Given a list of ingredients it recommends k recipes,
# by using the KNN algorithm.
#
#########################################################

# Python Modules
from collections import defaultdict

# K-dtree Library Modules
import kdtree

# Project Modules
from recipe import Recipe
from ingredient import Ingredient

class Recommender:
	""" Recipes Recommender """

	def __init__(self, recipes):

		self.recipes         = recipes
		self.recipes_dic     = defaultdict(list)
		self.ingredients_dic = self.extract_ingredients(recipes)
		self.ingredients     = self.ingredients_dic.keys()
		# self.ingredients_dic = ingredients_dic


	def get_recipes(self):
		""" Return the dictionary of recipes """

		return self.recipes_dic


	def extract_ingredients(self, recipes):
		""" Creates a dictionary with the ingredients found in the given recipes 
		    keeping the maximum quantity found for each ingredient to normalize later"""

		dic = {}

		for recipe in recipes:

			# Rank the ingredients
			ranked_ingredients = recipe.rank_ingredients()

			for ingredient in recipe.ingredients:

				ingredient_name = ingredient.name

				if ingredient_name != "undifined":
					if ingredient_name in dic:
						if ingredient.quantity > dic[ingredient_name]:
							dic[ingredient_name] = ingredient.quantity
					else:
						dic[ingredient_name] = ingredient.quantity

		return dic


	def read_query(self, file_name):
		""" Reads a list of ingredients from a file to find recipe recommendations later.
		    Assumes ingredients are all singular words (ex: apple instead of apples) """

		ingredients = {}

		with open(file_name, 'r') as f:
			for line in f:
				ingr = line.rstrip('\n')
				ingredients[ingr.lower()] = float(1)

		return ingredients


	def _create_point(self, names, query):
		""" Creates a point of ingredients' quantity for the given recipe """

		point = []

		for ingr in self.ingredients :

			# Save quantity of ingredient in current recipe
			if ingr in names:
				if not query:
					normalized = names[ingr] / self.ingredients_dic[ingr]
					point.append( normalized )
				else: # Put max quantity to requested ingredient
					point.append( float(1) )
				#point.append(float(1))
			else:
				point.append(float(0))

		return tuple(point)



	def create_points(self):
		""" Create the points that represent each recipe """

		points = []

		for recipe in self.recipes:

			names        = recipe.name_ingredients()
			recipe_point = self._create_point(names, query=False)
			points.append(recipe_point)

			# Save a dictionary of recipes according to these points
			self.recipes_dic[recipe_point].append( recipe.name )

		return points


	def _create_kdtree(self):
		""" Creates the KDTree of ingredients """

		#tree = kdtree.create(dimensions = len(ingredients))

		# For each recipe we create an array that indicates
		# if the recipe contains 1 a given ingredient or not 0
		# --> each array becomes a point in the tree
		points = self._create_points()

		return kdtree.create(points[:])


	def _remove_duplicates(self, l):
		""" Remove duplicate points in list l """

		new_list = []

		for elem in l:
			if new_list.count(elem) == 0:
				new_list.append(elem)

		return new_list

	def knn(self, tree, point, k):
		""" Return a list with the k nearest neighbours for given point """

		neighbours         = defaultdict(list)
		nearest_neighbours = []

		for node in list(tree.inorder()):
			dist = node.dist(point)
			neighbours[dist].append(node.data)

		in_order = sorted(neighbours)

		for elem in in_order[:k]:
			for node in neighbours[elem]:
				nearest_neighbours.append(node)

		return nearest_neighbours


	def point_recipe(self, clusters):
		""" Translates points in clusters with corresponding recipe name """

		recipe_clusters = defaultdict(list)
		c = 0

		for cluster in clusters.values():
			for point in cluster:
				for recipe in self.recipes_dic[point]:
					recipe_clusters[c].append(recipe)
			c += 1

		return recipe_clusters


	def get_recommendation(self, ingredients, k):
		""" Returns a list of k recommended recipes given some ingredients"""

		# Creates the KDTree of ingredients:
		# For each recipe we create an array that indicates
		# the quantity of each known ingredient on that recipe
		# --> each array becomes a point in the tree
		points = self.create_points()
		tree   = kdtree.create(points)

		# Create a point according to selected ingredients
		point  = self._create_point(ingredients, query=True)

		# Get matching recipes
		result       = self.knn(tree, point, k) #tree.search_knn(point, k)
		best_recipes = []
		for point in result:
			for r in self.recipes_dic[point]:
				best_recipes.append(r)

		return self._remove_duplicates(best_recipes)


	#h
	