######################################################
#
# TUM Machine Learning 
# Final Project : Recipes Classification
# 
# Author: Oriana Baldizan
# Data:   February 2015
#
# recipe.py : defines the Recipe class
#
# A Recipe consists of a name, a list of ingredients
# and a cooking process.
#
######################################################

# Python Modules
import operator
from collections import defaultdict

# Project Modules
from ingredient import Ingredient

class Recipe:
	""" Recipe """

	def __init__(self, name, ingr, process):

		self.name         = name
		self.ingredients  = ingr
		self.cook_process = process

	def _merge_ingredients(self):
		""" Sum the quantities of ingredients with the same name, 
		    but given in different tags in recipe """

		ingr_dic = {}

		for ingredient in self.ingredients:
			ingredient.convert_to_cup()

			if ingredient.name in ingr_dic:
				ingr_dic[ingredient.name] += ingredient.quantity
			else:
				ingr_dic[ingredient.name] = ingredient.quantity

		for ingredient in self.ingredients:
			ingredient.quantity = ingr_dic[ingredient.name]



	def rank_ingredients(self):
		""" Rank the ingredients by quantity """

		# for ingredient in self.ingredients:
		# 	ingredient.convert_to_cup()

		self._merge_ingredients()

		sorted_ingredients = sorted(self.ingredients, key=lambda x: x.quantity, reverse=True)

	 	return sorted_ingredients



	def name_ingredients(self):
		""" Returns a dictionary of recipe's ingredients """

		names_dic = {}

		for ingr in self.ingredients:
			name = ingr.name
			if name != "undifined":
				names_dic[name] = ingr.quantity

		return names_dic


	def print_recipe(self):
		""" Print recipe's information """

		print "Title: " + self.name
		print "Ingredients: "
		for ingredient in self.ingredients:
			ingredient.print_ingredient()
		# print "Preparation: " + self.cook_process



		