from collections import namedtuple
import itertools
from copy import copy

RED = "red"
ORANGE = "orange"
YELLOW = "yellow"
GREEN = "green"
BLUE = "blue"
VIOLET = "violet"

COLORS = {RED, ORANGE, YELLOW, GREEN, BLUE, VIOLET}
NUMBERS = range(1, 6)


def change_pcard(pcard, **kwargs):
	return pcard._replace(**kwargs)
	
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
		self._cards = self._cards + cards

	def cards_out(self, cards):
		'''
		removes cards from self._cards
		parameters:
			cards: a list of card objects
		'''
		cards_copy = copy(self._cards)
		for card in cards:
			cards_copy.remove(card)
		self._cards = cards_copy

class Supplier():

	def __init__(self, location, size = 1):
		self.size = size
		self.location = location

	def upgrade(self):
		self.size += 1

	def downgrade(self):
		self.size -= 1


class Supply():

	def __init__(self, cards =[]):
		self._cards = cards

	def cards_out(self, out_cards):
		the_cards = self._cards[:out_cards]
		del self._cards[:out_cards]
		return the_cards

	def cards_in(self, cards):
		self._cards = self._cards + cards
		



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
		old_neighbors = [self.find_pcard(card for card in self.get_neighbors(pcard))]

		new_pcard = change_pcard(pcard, card = new_card)
		new_neighbor_south = change_pcard(self.find_pcard(pcard.south), north = new_card)
		new_neighbor_north = change_pcard(self.find_pcard(pcard.north), south = new_card)
		new_neighbor_west = change_pcard(self.find_pcard(pcard.west), east = new_card)
		new_neighbor_east = change_pcard(self.find_pcard(pcard.east), west = new_card)
		new_neighbors = [new_neighbor_east, new_neighbor_west, new_neighbor_north, new_neighbor_south]

		self._cards = self._cards + new_neighbors

		for index in range(len(old_neighbors)):
			old = old_neighbors[index]
			if old in self._cards:
				self._cards.remove(old)

		self._cards.remove(pcard)
		self._cards = self._cards + [new_pcard]


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
		home_card = company._supplier.location
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
		self.name = name
		self._hand = hand
		self._supplier = supplier

	def take_turn(self, supply, catalog):

		TeaCards.take_turn()

	def supply(self, supply):

		hand = self._hand
		size = self._supplier.size
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

	def operate(self, supply, catalog):
		""" increases a company's hand size by either the company's line_size or supplier, whichever is smallest """
		supplier = self._supplier
		line_size = len(catalog.get_line(self))
		difference = line_size - supplier.size

		if difference == 1 or difference == 0:
			self.draw(supply, supplier.size)
		elif difference >= 2:
			company.supplier -= 1
			self.draw((supplier - 2)),
		elif difference == -1:
			self.draw(line_size)
		elif difference <= -2:
			company.supplier -= 1
			self.draw(line)

class TeaCards():

	def __init__(self, catalog, companies, supply):
		self._catalog = catalog
		self._companies = companies
		self._supply = supply
		self._turn_takers = repeat(companies)

	def take_turn(self):
		turn_taker = next(self._turn_takers)
		catalog, supply = turn_taker.take_turn()
		self._catalog = catalog
		self._supply = supply

		if turn_taker.loses_to(self._companies):
			self.eliminate_company(turn_taker)

	def eliminate_company(self, company):
			self._companies.pop(turn_taker)
			self._turn_takers = repeat(self._companies)

	def initiate_game(self, deck_file, companies,catalog_shape):

		def get_deck(deck_file):
			with open(deck_file) as f:
				r = np.genfromtxt(f,dtype=str, delimiter = ',')
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


