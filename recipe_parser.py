######################################################
#
# TUM Machine Learning 
# Final Project : Recipes Classification
# 
# Author: Oriana Baldizan
# Data:   February 2015
#
# recipe_parser.py : XML parser for the recipes
#
######################################################

# Python Modules
import re
import itertools
import xml.etree.ElementTree as ET
from fractions import Fraction

# Textblob Library Modules
from textblob import Word
from textblob import TextBlob
# from nltk.corpus import wordnet as wn

# Project Modules
from recipe import Recipe
# from product import Product
from ingredient import Ingredient


class Parser:
	""" XML Parser """

	def __init__(self, data_file, dictionary):
		""" Creates the parser tree """

		self.tree       = ET.parse(data_file)
		self.root       = self.tree.getroot()
		self.dictionary = dictionary  # Food tree

		self.unit_measures = {
			"c":"cup", "C":"cup", "cup":"cup",
			"cn":"can", "CN": "can", "can":"can",
			"t":"tsp", "teaspoon":"tsp", "tspn":"tsp", "tsps":"tsp", "tsp":"tsp", "ts":"tsp",
			"T":"tbsp", "tablespoon":"tbsp", "tbsps":"tbsp", "tbsp":"tbsp", "tbs":"tbsp", "tb":"tbsp", "Tblsp":"tbsp", "Tsp":"tbsp",
			"pounds":"lb", "lbs":"lb", "lb":"lb",
			"quarts":"qt", "quart":"qt", "qts":"qt", "qt":"qt", "q":"qt",
			"pint":"pt", "pts":"pt", "pt":"pt", "p":"pt",
			"oz":"oz", "ounce":"oz", "fluid ounce":"oz", "f oz":"oz",
			"gallon":"gal", "gal":"gal", "gals":"gal",
			"g":"gr", "gr":"gr", "gram":"gr",
			"mg":"mg", "miligram":"mg",
			"kg":"kg", "kilogram":"kg",
			"l":"l", "liter":"l",
			"ml":"ml", "mililiter":"ml",
			"pinch":"pinch",
			"dash":"dash", "ds":"dash",
			"drop":"drop",
			"touch":"touch",
			"clove":"clove",
			"ea":"each"
		}


	def _parse_product(self, description):
		""" Parse ingredient's products """

		return Product(name, unit, format, quantity)


	def _food_concept(self, combinations):
		""" Return a list of food concepts found in all combinations """
		concepts = []

		for comb in combinations:
			c = " ".join(comb)
			if c in self.dictionary:
				concepts.append(c)

		if len(concepts) == 0:
			concepts.append("undifined")

		return concepts


	def _all_combinations(self, word_list):
		""" Generates a list of all possible word combinations in word_list """

		combinations = []
		for word in range(0, len(word_list)+1):
			for subset in itertools.combinations(word_list, word):
				if len(subset) > 0:
					combinations.append(list(subset))

		return combinations


	def _extract_name(self, word_list):
		""" Only keep the words that form a concept of the food tree """
		
		text = " ".join(word_list)
		text = re.sub('[^a-zA-z0-9\s]', '', text) # Remove any extra character
		word_list = text.split(" ")

		# Keep the combination of words that define a food concept
		combinations = self._all_combinations(word_list)
		name         = self._food_concept(combinations).pop() # Guarantees the most specific concept

		return name


	# def _is_unit(self, word):
	# 	""" Checks if the word is a unit measure 1 or not 0 """

	# 	for measure in self.unit_measures:
	# 		if measure == word:
	# 			return True

	# 	return False


	def _to_float(self, s):
		""" String s to float """

		if '/' in s:
			return float(Fraction(s))
		else:
			return float(s)

		# try:
		# 	number = float(s)
		# 	return number
		# except ValueError:
		# 	return float(Fraction(s))


	def _parse_ingredient(self, description):
		""" Parse the ingredient information """

		# ingredients = []
		blob        = TextBlob(description)
		name_words  = []

		quantity    = float(0)
		format      = ""
		name        = ""
		unit        = ""
		for word in blob.tags:

			# Extract ingredient quantity
			if word[1] == unicode('CD') or word[0] == '2':
				if re.sub('[a-zA-Z\s]', '', word[0]) != '':
					quantity = float(1)
					quantity = quantity * self._to_float(word[0])

			# Extract unit measurement and name
			elif word[1] in ("NN", "NNS", "NNP", "NNPS", "VBG", "JJ"):
				if str(word[0]) == "flour":
					w = str(word[0])
				else:
					w = str(word[0].singularize())

				if w in self.unit_measures:
					unit = self.unit_measures[w]
				else:
					name_words.append(w)

			# Extract format
			else:
				format += str(word[0])

		if unit == "":
			unit = "each"

		if quantity == float(0):
			unit     = "each"
			quantity = 1

		name       = self._extract_name(name_words)
		ingredient = Ingredient(name, unit, quantity, format, description)

		return ingredient



	def _separate(self, description):
		""" Separate description according to number of optional ingredients """

		new_descriptions = []

		description = re.sub('[^a-zA-Z0-9\s/]', '', description) # Remove any extra character
		description = description.replace(" or ", " ") # Remove OR

		# Extract all the optional ingredients
		combinations = self._all_combinations(description.split(" "))
		all_names    = self._food_concept(combinations)

		for name in all_names:
			new_desc = description

			for other in all_names:

				for word in other.split(" "):
					new_desc = new_desc.replace(word, "")

			new_desc = name + " " + new_desc + " OR "
			new_descriptions.append(new_desc)

		return new_descriptions


	def generate(self):
		""" Generates a List of recipes From the XML"""

		recipes = []

		for child in self.root.findall('recipe'):
			name        = child.find('ti').text
			process     = child.find('pr').text

			ingredients = []
			for i in child.findall('in'):
				description = i.text.lower()

				if " or " in description: # We have different options in one
					options = self._separate(description)

					for option in options:
						ingredient = self._parse_ingredient(option)
						ingredients.append(ingredient)

				else:
					ingredient = self._parse_ingredient(description)
					ingredients.append(ingredient)

			recipe = Recipe(name.lower(), ingredients, process.lower())
			recipes.append(recipe)

		return recipes