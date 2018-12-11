from collections import namedtuple
import itertools
from copy import copy, deepcopy
from itertools import cycle, islice

RED = "red"
ORANGE = "orange"
YELLOW = "yellow"
GREEN = "green"
BLUE = "blue"
VIOLET = "violet"

COLORS = {RED, ORANGE, YELLOW, GREEN, BLUE, VIOLET}
NUMBERS = range(1, 6)


def change_pcard(pcard, **kwargs):
	new_pcard = pcard._replace(**kwargs)
	return new_pcard
	
def is_in(card, cards):
	for c in cards:
		if card is c:
			return True
	return False

def flatten(lists):
	return list(itertools.chain(*lists))

class Card():
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
	""" contains cards as unordered Counter() object of namedtuples"""

	def __init__(self, cards = []):
		self._cards = cards

	def cards_in(self, cards):
		'''
		updates self._cards with new cards
		parameters:
			cards: a list of card objects
		'''
		return Hand(cards = self._cards + cards)

	def cards_out(self, cards):
		'''
		removes cards from self._cards
		parameters:
			cards: a list of card objects
		'''
		cards_copy = copy(self._cards)
		for card in cards:
			cards_copy.remove(card)
		return Hand(cards = cards_copy)

class Supplier():

	def __init__(self, location, size = 1):
		self._size = size
		self._location = location

	def upgrade(self):
		return Supplier(size = self._size + 1, location = self._location)

	def downgrade(self):
		return Supplier(size = self._size - 1, location = self._location)


class Supply():

	def __init__(self, cards =[]):
		self._cards = cards

	def draw(self, out_cards):
		the_cards = self._cards[:out_cards]
		return the_cards

	def cards_out(self, out_cards):
		return Supply(cards = self._cards[out_cards:])

	def cards_in(self, cards):
		return Supply(cards = self._cards + cards)
		



class Catalog():

	def __init__(self, positioned_cards):
		self._cards = positioned_cards

	def find_pcard(self, card):
		"""searcher self._cards for positioned card with card as main card. If this p-card does not exist it makes one with default attributes
		
		"""
		pcard = [pcard for pcard in self._cards if pcard.card == card]
		if pcard == []:
			pcard = [PositionedCard(card = card)]
		return pcard[0]

	def swap(self, old_card, new_card):
		""" updates p-card of old_card with card = card, and updates its neighbors to match. Then writes these to pcards and removes the old_pcard and neighbors
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
		return set(flatten([self.line_of_color(home_card, color, pcards) for color in colors]))


class Company():
	"""
	attributes:
		name: str unique to Company instance
		hand: a list of Card objects
		supplier: an Supplier object with size and location
	"""

	def __init__(self, supplier, name = '', hand = []):
		self._name = name
		self._hand = hand
		self._supplier = supplier

	def supply(self, supply):

		hand = self._hand
		size = self._supplier._size
		supply.cards_in(hand)
		self._hand = []
		self._supplier.upgrade()

	def trade(self, catalog, supply, old_card, new_card, payment_cards):
		cost = max(old_card._number, new_card._number)
		self._hand.cards_out(payment_cards)
		supply.cards_in(payment_cards)
		catalog.swap(old_card, new_card)
		supply.cards_in([old_card])
		self._hand.cards_out([new_card])

	def draw(self, supply, number_of_cards):
		the_cards = supply.cards_out(number_of_cards)
		self._hand.cards_in(the_cards)
'''
	def operate(self, company, supply, catalog):
		""" increases a company's hand size by either the company's line_size or supplier, whichever is smallest """
		supplier = company._supplier._size
		line_size = len(catalog.get_line(self))
		difference = line_size - supplier._size
		hand = company._hand

		if difference == 1 or difference == 0:
			new_supply = supply.cards_out(line_size)
			new_hand = hand.in
		elif difference >= 2:
			company.supplier -= 1
			self.draw((supplier - 2)),
		elif difference == -1:
			self.draw(line_size)
		elif difference <= -2:
			company.supplier -= 1
			self.draw(line)'''

class TeaCards():

	def __init__(self, catalog, companies, supply):
		self._catalog = catalog
		self._companies = companies
		self._supply = supply
		self._turn_takers = cycle(companies)

	def take_turn(self):
		turn_taker = next(self._turn_takers)
		catalog, supply = turn_taker.take_turn()
		self._catalog = catalog
		self._supply = supply

		if turn_taker.loses_to(self._companies):
			self.eliminate_company(turn_taker)

	def eliminate_company(self):
			self._companies.pop(turn_taker)
			self._turn_takers = repeat(self._companies)

	def get_company(self, company):
		return self._companies[self._companies.index(company)]

	def replace_company(self, company, new_company):
		self._companies[self._companies.index(company)] = new_company




	def supply(self, company):
		new_supply = self._supply.cards_in(company._hand)
		new_supplier = company._supplier.upgrade()

		new_company = deepcopy(company)
		new_company._supplier = new_supplier
		new_company._hand = []
		self._supply = new_supply
		self.replace_company(company, new_company)

	def trade(self, company, catalog, supply, old_card, new_card, payment_cards):
		cost = max(old_card._number, new_card._number)
		new_hand = company._hand.cards_out(payment_cards + [new_card])
		new_supply = supply.cards_in(payment_cards + [old_card])
		new_catalog = catalog.swap(old_card, new_card)

		new_company = deepcopy(company)
		new_company._hand = new_hand

		self.replace_company(company, new_company)
		self._supply = new_supply
		self._catalog = new_catalog

	def operate(self, company, supply, catalog):
		""" increases a company's hand size by either the company's line_size or supplier, whichever is smallest """
		supplier = company._supplier
		size = supplier._size
		line_size = len(catalog.get_line(company))
		difference = line_size - supplier._size
		hand = company._hand

		if difference == 1 or difference == 0:
			hand = hand.cards_in(supply.draw(size))
			supply = supply.cards_out(size)
		elif difference >= 2:
			print('over operation')
			supplier = supplier.downgrade()
			hand = hand.cards_in(supply.draw(size - 2))
			supply = supply.cards_out(size - 2)
		elif difference == -1:
			print('just under operate')
			hand = hand.cards_in(supply.draw(line_size))
			supply = supply.cards_out(line_size)
		elif difference <= -2:
			print('underoperate')
			supplier = supplier.downgrade()
			hand = hand.cards_in(supply.draw(line_size))
			supply = supply.cards_out(line_size)

		new_company = deepcopy(company)
		new_company._hand = hand
		new_company._supplier = supplier
		self.replace_company(company, new_company)
		self._supply = supply

	def initiate_game(self, deck_file, companies,catalog_shape):

		def get_deck(deck_file):
			with open(deck_file) as f:
				r = np.genfromtxt(f, dtype=str, delimiter = ',')
				deck = []
				for i in range(len(r)):
					colors = set(r[i][0].split(' '))
					number = int(r[i][1])
					deck.append(Card(colors,number))
			return deck

		self.supply = get_deck(deck_file)

		get_deck(deck_file)

		def build_catalog(decK):
			pass

		build_catalog(self.supply)


