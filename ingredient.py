######################################################
#
# TUM Machine Learning 
# Final Project : Recipes Classification
# 
# Author: Oriana Baldizan
# Data:   February 2015
#
# ingredient.py : defines the Ingredient class
#
# An Ingredient consists of a name, description, quantity,
# unit format (specific instruction, ex: chopped), a
# level of relevance, and an isOptional attribute.
#
######################################################

# from product import Product

class Ingredient:
	""" Ingredient """

	def __init__(self, name, unit, quantity, format, description):

		# self.products    = products
		self.name        = name
		self.unit        = unit
		self.level       = 1
		self.format      = format
		self.quantity    = quantity
		self.isOptional  = 1 if description.find(" OR ") != -1 else 0
		self.description = description

		# 1 cup is 48 teaspoons (tsp)
		self.conversions = {
		"cup":float(1.0),
		"can":float(1.0),
		"tsp":float(48.0),
		"tbsp":float(16.0),
		"lb":float(0.00779),
		"qt":float(0.25),
		"pt":float(0.5),
		"oz":float(8.0),
		"gal":float(0.0625),
		"gr":float(3.5437),
		"mg":float(3543.7),
		"kg":float(0.00354),
		"l":float(0.236),
		"ml":float(236.59),
		"pinch":float(768.0),
		"dash":float(384.0),
		"drop":float(2880.0),
		"touch":float(2000.0),
		"clove":float(96.0),
		"each":float(8)
		}

	def convert_to_cup(self):
		""" Convert quantity to cup unit quantity """

		self.quantity = self.quantity / self.conversions.get(self.unit, 1)


	def convert_to_original(self):
		""" Conver quantity to original unit """

		self.quantity = self.quantity * self.conversions.get(self.unit, 1)


	def print_ingredient(self):
		""" Prints ingredient's information """

		print "  - " + self.name + " : " + str(self.quantity) + " " + self.unit


	# def _level_products():

	# 	sorted_products = sorted(self.products, key=attrgetter('quantity'), reverse=True)
	# 	return sorted_products
