from collections import namedtuple
import numpy as np
import csv
import random
class Card(object):
	def __init__(self, colors, number):
		self.colors=colors
		self.number=number

class Company(object):

	def __init__(self, hand = [], supplier = 6, line = [], location = (0,0)):
		self.hand = hand
		self.supplier = supplier
		self.line = line
		self.location = location

'''
def get_deck(deck_file):
	"""
	parameters: deck_file.: a .csv file wih line of form 'color colr, number'
				entered with quotes ""
	returns: a list of named tuples with colors =set(colors), number =int(number)
	"""
	card = namedtuple('card',['colors','number'])
	with open(deck_file,'r') as f:
		r = csv.reader(f, delimiter=',')
		cards = []
		rows = [card(*l) for l in r]
		for row in rows:
			color = set(row.colors.split(' '))
			num = int(row.number)
			cards.append(card(color,num))
	return cards
'''

def build_deck(deck_file):
	'''
	parameters: deck_file: a .csv or .txt file with cards in lines
				of form: color1 color2, number
	returns: a  randomized list of Card objects with attributes
				.colors = {color1, color2}
				.number = int(number)
	'''
	with open(deck_file) as f:
		r = np.genfromtxt(f,dtype=str, delimiter = ',')
		deck = []
		for i in range(len(r)):
			colors = set(r[i][0].split(' '))
			number = int(r[i][1])
			deck.append(Card(colors,number))
	return random.sample(deck, len(deck))

def build_catalog(deck, size = (3,3)):
	"""
	parameter deck: the result of a build_deck call. A list of Card obects
	parameter size: The nxm size of the resulting array.
	resturn: an array of size size[0]xsize[1] array drawn from the top
			of the deck. Also mutates deck respectively 
	"""
	number_of_cards = size[0] * size[1]
	catalog = np.reshape(np.array(deck[:number_of_cards]),(size[0],size[1]))
	del deck[:number_of_cards]
	return catalog

def get_line(company, catalog):
	company.line = [catalog[company.location[0]][company.location[1]]]
	line = company.line
	company_colors = catalog[company.location[0]][company.location[1]].colors
	def get_line_card(line_colors, location):
		i = location[0]
		j = location[1]
		neighbors = [(i+1,j),(i-1,j),(i,j+1),(i,j-1)]
		for neighbor in neighbors:
			x = neighbor[0]
			y = neighbor[1]
			if (x in range(len(catalog[0]))) and (y in range(len(catalog))):
				common_colors = line_colors.intersection(catalog[x][y].colors)
				if len(common_colors) > 0:
					if catalog[x][y] not in company.line:
						company.line.append(catalog[x][y])
						return get_line_card(common_colors, (x,y))
	get_line_card(company_colors, company.location)
	return company.line

'''
for card in get_line(comp):
	i, j = np.where(catalog == card)
	print(card.colors, i,j, )
print(get_line(comp))
'''
