from collections import namedtuple
import itertools
from copy import copy, deepcopy
from itertools import cycle, islice
import random

RED = "red"
ORANGE = "orange"
YELLOW = "yellow"
GREEN = "green"
BLUE = "blue"
VIOLET = "violet"

COLORS = {RED, ORANGE, YELLOW, GREEN, BLUE, VIOLET}
NUMBERS = range(1, 6)


def change_pcard(pcard, **kwargs):
	'''
	return a copy of PositionedCard, pcard, with key-word arguments replaced with kwargs
	'''
	new_pcard = pcard._replace(**kwargs)
	return new_pcard
	
def is_in(card, cards):
	'''
	determines whether an element is in a list
	'''
	for c in cards:
		if card is c:
			return True
	return False

def flatten(lists):
	'''
	flattens list
	'''
	return list(itertools.chain(*lists))

class Card():
	'''
	attributes:
		colors: set of colors, {COLOR, COLOR}
		number: an integer
	'''
	def __init__(self, colors, number):
		self._colors=colors
		self._number=number

	def __str__(self):
		return "%s  %s" % (self._colors, self._number)

PositionedCard = namedtuple(
	"PositionedCard",
	['card', 'north', 'south', 'east', 'west'])
default_card = Card(colors = {None}, number = 64)
PositionedCard.__new__.__defaults__ = (default_card, default_card, default_card, default_card, default_card)

class Hand():
	""" contains cards as list of Card objects"""

	def __init__(self, cards = []):
		self._cards = cards

	def cards_in(self, cards):
		'''
		returns a copy of self with cards added
		parameters:
			cards: a list of card objects
		'''
		return Hand(cards = self._cards + cards)

	def cards_out(self, cards):
		'''
		returns a copy of self with cards removed
		parameters:
			cards: a list of card objects
		'''
		cards_copy = copy(self._cards)
		for card in cards:
			cards_copy.remove(card)
		return Hand(cards = cards_copy)

class Supplier():
	'''
	attributes:
		size: an integer
		location a Card object
	'''
	def __init__(self, location, size = 1):
		self._size = size
		self._location = location

	def upgrade(self):
		''' returns a Supplier object with size attirbute increased by 1 '''
		return Supplier(size = self._size + 1, location = self._location)

	def downgrade(self):
		''' returns a Supplier object with size attirbute decreased by 1 '''
		return Supplier(size = self._size - 1, location = self._location)


class Supply():
	'''
	attribute:
		cards: list of card objects
	'''

	def __init__(self, cards =[]):
		self._cards = cards

	def draw(self, out_cards):
		'''
		parameters:
			out_cards: integer representing number of cards to draw
		returns the top out_cards number of cards from the supply
		'''
		the_cards = self._cards[:out_cards]
		return the_cards

	def cards_out(self, out_cards):
		'''
		parameters:
			out_cards: integer representing number of cards to draw
		returns copy of self with out_card number of cards removed
		'''
		return Supply(cards = self._cards[out_cards:])

	def cards_in(self, cards):
		''' returns copy of self with cards added '''
		return Supply(cards = self._cards + cards)
		



class Catalog():

	def __init__(self, positioned_cards):
		self._cards = positioned_cards

	def find_pcard(self, card):
		"""searches self._cards for positioned card with card as main card. If this p-card does not exist it makes one with default attributes
		"""
		pcard = [pcard for pcard in self._cards if pcard.card == card]
		if pcard == []:
			pcard = [PositionedCard(card = card)]
		return pcard[0]

	def swap(self, old_card, new_card):
		""" updates p-card of old_card with card = new_card, and updates its neighbors to match. Then writes these to pcards and removes the old_pcard and neighbors
		paramenters:
			old_card: Card object
			new_card: Card object
		returns a copy of self with the pcards updated
		"""
		pcard = self.find_pcard(old_card)
		old_neighbors = [self.find_pcard(card) for card in self.get_neighbors(pcard)]
		
		new_pcard = change_pcard(pcard, card = new_card)
		new_neighbor_south = change_pcard(self.find_pcard(pcard.south), north = new_card)
		new_neighbor_north = change_pcard(self.find_pcard(pcard.north), south = new_card)
		new_neighbor_west = change_pcard(self.find_pcard(pcard.west), east = new_card)
		new_neighbor_east = change_pcard(self.find_pcard(pcard.east), west = new_card)
		new_neighbors = [new_neighbor_east, new_neighbor_west, new_neighbor_north, new_neighbor_south]
		new_cards = self._cards + new_neighbors
		new_cards = [card for card in new_cards if card.card != default_card and card not in old_neighbors]

		new_cards.remove(pcard)
		new_cards = new_cards + [new_pcard]
		return Catalog(positioned_cards = new_cards)


	def get_neighbors(self, pcard):
		"""return list of neighbors of pcard"""
		return [pcard.north, pcard.south, pcard.east, pcard.west]
	
	def matching_neighbors(self, pcard, color, line = []):
		""" returns list of neighbors which match the color """
		return [card for card in self.get_neighbors(pcard) if color in card._colors and card not in line]

	def line_of_color(self,card, color, pcards, line = []):
		""" returns a list of cards which are in a line of cards each matching the color"""
		pcard = self.find_pcard(card)
		matching_neighbors = self.matching_neighbors(pcard, color, line)
		if matching_neighbors == []:
			return line
		return [self.line_of_color(card, color, pcards, (line + matching_neighbors)) for card in matching_neighbors][0]

	def get_line(self, company):
		""" returns combined line_or_color for each color on company's home-card"""
		pcards = self._cards
		home_card = company._supplier._location
		colors = home_card._colors
		return set(flatten([self.line_of_color(home_card, color, pcards) for color in colors]) + [home_card])


class Company():
	"""
	attributes:
		name: str unique to Company instance
		hand: a list of Card objects		supplier: an Supplier object with size and location
	"""

	def __init__(self, supplier, player = None, name = '', hand = Hand(cards = []), deck = ''):
		self._name = name
		self._hand = hand
		self._supplier = supplier
		self._deck = deck
		self._player = player

	def get_deck(deck_file):
		''' builds a list of card objects
		parameters:
			deck_file: a csv file containing lines of form {COLOR, COLOR}, number
		returns a list of Card objects obtained from the deck_file
		'''
		with open(deck_file) as f:
			r = np.genfromtxt(f, dtype=str, delimiter = ',')
			deck = []
			for i in range(len(r)):
				colors = set(r[i][0].split(' '))
				number = int(r[i][1])
				deck.append(Card(colors = colors, number = number))
		return deck


class TeaCards():
	'''
	attriubtes:
		catalog: a Catalog object
		companies: a list of companie objects
		supply: a Supply object
	'''

	def __init__(self, catalog = Catalog(positioned_cards = []), companies = [], supply = Supply(cards = []), turn_taker = None):
		self._catalog = catalog
		self._companies = companies
		self._supply = supply
		self._turn_taker = turn_taker
		self._turn_takers = cycle(companies)

	def take_turn(self, turn_taker):
		''' takes user input to perform a turn action.
		parameters: 
			turn_taker: a Company object
		returns a call to take_turn with next turn taker in list of companies
		'''
		action = input("What would you like to do? operate, trade, or supply")

		if action == 'operate':
			supply = self._supply
			catalog = self._catalog
			new_tea_cards = self.operate(turn_taker, supply, catalog)

		elif action == 'supply':
			new_company = self.supply(turn_taker)

		elif action == 'trade':
			old_card = input("Which card would you like to replace?")
			new_card = input("Which card would you like to replace it with?")
			payment_cards = input("Which cards would you like to pay with?")
			supply = self._supply
			catalog = self._catalog

			new_tea_cards = self.trade(turn_taker, catalog, supply, old_card, new_card, payment_cards)
		else:
		 return self.take_turn(turn_taker)

		company_sizes = [comp._supplier._size for comp in new_tea_cards._companies]
		if max(company_sizes) - turn_taker._supplier._size >= 2:
			new_tea_cards._companies.pop(turn_taker)
		if len(self.companies) == 1:
			return endgame()
		next_turn_taker = next(new_tea_cards._turn_takers)
		return new_tea_cards.take_turn(next_turn_taker)

	def get_company(self, company):
		return self._companies[self._companies.index(company)]

	def replace_company(self, company, new_company):
		''' returns a copy of self.companies with company replaced by new_company '''
		companies = deepcopy(self._companies)
		companies[self._companies.index(company)] = new_company
		return companies

	def supply(self, company, tea_cards):
		''' empties a copmanies hand in to the supply and upgrades the company's supplier '''
		hand = company._hand
		size = company._supplier._size
		try:
			hand._cards[size]
		except IndexError:
			('not enough cards')
			return self
		else:
			new_supply = self._supply.cards_in(company._hand._cards)
			new_supplier = company._supplier.upgrade()

			new_company = deepcopy(company)
			new_company._supplier = new_supplier
			new_company._hand = []
			new_companies = tea_cards.replace_company(company, new_company)

			turn_taker = next(tea_cards._turn_takers)

			return TeaCards(supply = new_supply, catalog = self._catalog, companies = new_companies, turn_taker = turn_taker)

	def trade(self, tea_cards, company, catalog, supply, old_card, new_card, payment_cards):
		''' replaces a card in the catalog with a card from a hand 
		parameters:
			company: a Company object
			catalog: a Catalog object
			supply: a Supply object
			old_card: Card object that is in the catalog
			new_card: Card object that is the company's hand
			payment_cards: list of Card objects that are in company's hand
		returns a copy of self with catalog update with new_card
		'''
		hand = company._hand
		cost = max(old_card._number, new_card._number)
		try:
			hand._cards[cost - 1]
		except IndexError:
			('not enough cards')
			return self
		else:
			new_hand = company._hand.cards_out(payment_cards + [new_card])
			new_supply = supply.cards_in(payment_cards + [old_card])
			new_catalog = catalog.swap(old_card, new_card)

			new_company = deepcopy(company)
			new_company._hand = new_hand
			new_companies = self.replace_company(company, new_company)

			turn_taker = next(tea_cards._turn_takers)

			
			return TeaCards(supply = new_supply, catalog = new_catalog, companies = new_companies, turn_taker = turn_taker)


	def operate(self, tea_cards, company, supply, catalog):
		""" increases a company's hand size by either the company's line_size or supplier, whichever is smallest 
		parameters:
			company: Company object
			supply: Supply object
			catalog: Catalog object
		returns a copy of self with cards added to company, and removed from supply. Downgrades company supplier if supplier's size is too far from the size of its line
		"""
		supplier = company._supplier
		size = supplier._size
		line_size = len(catalog.get_line(company))
		difference = line_size - supplier._size
		hand = company._hand

		if difference == 1 or difference == 0:
			new_hand = hand.cards_in(supply.draw(size))
			new_supply = supply.cards_out(size)
			new_supplier = supplier

		elif difference >= 2:
			new_supplier = supplier.downgrade()
			new_hand = hand.cards_in(supply.draw(size - 2))
			new_supply = supply.cards_out(size - 2)

		elif difference == -1:
			new_hand = hand.cards_in(supply.draw(line_size))
			new_supply = supply.cards_out(line_size)
			new_supplier = supplier

		elif difference <= -2:
			new_supplier = supplier.downgrade()
			new_hand = hand.cards_in(supply.draw(line_size))
			new_supply = supply.cards_out(line_size)

		new_company = deepcopy(company)
		new_company._hand = new_hand
		new_company._supplier = new_supplier
		new_companies = tea_cards.replace_company(company, new_company)

		max_supplier = max([comp._supplier._size for comp in new_companies])

		if new_supplier._size == 0 or max_supplier - new_supplier._size >= 2:
			new_companies.remove(new_company)

		turn_taker = next(tea_cards._turn_takers)

		return TeaCards(supply = new_supply, catalog = catalog, companies = new_companies, turn_taker = turn_taker)

	def build_supply(self, companies):
		supply = []
		for company in companies:
			supply = supply + company.build_deck(company._deck)
		return random.sample(supply, len(supply))

	def play(self, tea_cards):
		number_of_players = len(tea_cards._companies)
		active_tea_cards = tea_cards

		while number_of_players > 1:
			turn_taker = active_tea_cards._turn_taker
			active_player = turn_taker._player
			active_tea_cards = active_player.take_turn(active_tea_cards, turn_taker)
			number_of_players = len(active_tea_cards._companies)

		winner = active_tea_cards._companies[0]._player
		return active_tea_cards.end_of_game(winner)

	def end_of_game(self, player):
		return print(player._name, 'has won')

class PlayerHuman():

	def __init__(self, name = ''):
		self._name = name

	def take_turn(self, tea_cards, company):
		''' takes user input to perform a turn action.
		parameters: 
			turn_taker: a Company object
		returns a call to take_turn with next turn taker in list of companies
		'''
		action = input("What would you like to do? operate, trade, or supply")

		if action == 'operate':
			supply = tea_cards._supply
			catalog = tea_cards._catalog
			return tea_cards.operate(tea_cards, company, supply, catalog)

		elif action == 'supply':
			return tea_cards.supply(tea_cards, company)

		elif action == 'trade':
			old_card = input("Which card would you like to replace?")
			new_card = input("Which card would you like to replace it with?")
			payment_cards = input("Which cards would you like to pay with?")
			supply = tea_cards._supply
			catalog = tea_cards._catalog

			return tea_cards.trade(tea_cards, company, catalog, supply, old_card, new_card, payment_cards)
		else:
			return self.take_turn(tea_cards, company)

		
			
#class PlayerComputer():






