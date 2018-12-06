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

Supplier = namedtuple("Supplier", ['location', 'size'])

def change_neighbor(pcard, **kwargs):
	vals = getattr(pcard).copy()
	vals.update(kwargs)
	return PositionedCard(**vals)

def upgrade_supplier(supplier, kwargs):
	vals = getattr(supplier).copy()
	vals.update(kwargs)
	return Supplier(vals)

class Hand(Object):

	def __init__(self, cards):
		self._cards = cards


	def cards_in(the_cards)
		self._cards += the_cards

	def cards_out(self, number_of_cards)
		self._cards -= number_of_cards


class Supply(Object):

	def __init__(self, cards):
		self._cards = cards

	def cards_out(self, number_of_cards):
		self._cards -= number_of_cards

	def cards_in(self, cards):
		self._cards += cards 
		


class Catalog(Object):

	def __init__(self, positioned_cards):
		self._cards = positioned_cards

	def swap(self, cards):
		change_neighbor(pcard, card = card)

	def get_line(self, location):
		pass
		


class Company(Object):

	def __init__(self, hand, supplier = 1):
		self._hand = hand
		self._supplier = supplier

	def take_turn(self):
		TeaCards.take_turn()

	def supply(self, supply, cards):
		supply.cards_in(cards)
		self._hand.cards_out()
		self.supplier = upgrade_supplier(self.supplier) 

	def trade(self, catalog, supply, cards):
		catalog.swap()
		self._hand.cards_out()

	def operate(self, supply, catalog):
		size_line = catalog.get_line(self.supplier.location)
		the_cards = supply.cards_out()
		self._hand.cards_in(the_cards)


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

	def initiate_game(self, deck_file, companies,catalog_shape):
		def get_deck(deck_file):
			pass

		self.supply = get_deck(deck_file)

		def build_catalog(decK):
			pass

		self.catalog = build_catalog(self.supply)


