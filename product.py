######################################################
#
# TUM Machine Learning 
# Final Project : Recipes Classification
# 
# Author: Oriana Baldizan
# Data:   February 2015
#
# product.py : defines the Product class
#
# A Product consists of a name, quantity, unit 
# format (specific instruction, ex: chopped), a
# level of relevance.
#
######################################################

class Product:
	""" Ingredient Product """

	def __init__(self, name, unit, format, quantity):

		self.name     = name
		self.unit     = unit
		self.level    = level
		self.format   = format
		self.quantity = quantity