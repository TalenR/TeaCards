from collections import namedtuple

RED = "red"
ORANGE = "orange"
YELLOW = "yellow"
GREEN = "green"
BLUE = "blue"
PURPLE = "purple"

COLORS = {RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE}
NUMBERS = range(1, 6)

Card = namedtuple("Card", ['colors','number'])

PositionedCard = namedtuple(
	"PositionedCard",
	['card', 'north', 'south', 'east', 'west'])

pcard = PositionedCard("card", "n", "s", "e", "w")
Supplier = namedtuple("Supplier", ['location', 'size'])

def change_neighbor(pcard, **kwargs):
	vals = pcard.__attrs__.copy()
	vals.update(kwargs)
	return PositionedCard(**vals)

class Hand(Object):

	def __init__(self, cards):
		self._cards = cards

	def draw_cards(self, supply):
		#self._cards.extend(cards)
		the_cards = supply.draw_cards()
		self.add_cards(the_cards)

	def add_cards(the_cards)
		self._cards = self._cards + the_cards


class Supply(Object):

	def __init__(self, cards):
		self._cards = cards

	def draw_cards(self, hand, number_of_cards)
		self._cards = self.cards - number_of_cards



class Catalog(Object):

	def __init__(self, positioned_cards):
		self._cards = 


class Company(Object):

	def __init__(self, hand, supplier):
		self._hand = hand
		self._supplier = supplier

	def take_turn(self):
		pass

	def operate(self, catalog):
		pass

	def trade(self, catalog, supply):
		pass

	def supply(self, supply):
		the_cards = supply.draw_cards(4)
		self._hand.cards_drawn(the_cards)


class TeaCards(Object):

	def __init__(self, catalog, companies, supply):
		self._catalog = catalog
		self._companies = companies
		self._supply = supply
		self._turn_takers = repeat(companies)

	def take_turn():
		turn_taker = next(self._turn_takers)
		catalog, supply = turn_taker.take_turn()
		self._catalog = catalog
		self._supply = supply

		if turn_taker.loses_to(self._companies):
			self.eliminate_company(turn_taker)

	def eliminate_company(company):
			self._companies.pop(turn_taker)
			self._turn_takers = repeat(self._companies)

			sdCc