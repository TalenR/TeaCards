from collections import namedtuple
import itertools

RED = "red"
ORANGE = "orange"
YELLOW = "yellow"
GREEN = "green"
BLUE = "blue"
PURPLE = "purple"

COLORS = {RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE}
NUMBERS = range(1, 6)

PositionedCard = namedtuple(
	"PositionedCard",
	['card', 'north', 'south', 'east', 'west'])
PositionedCard.__new__.__defaults__ = (None, None, None, None, None, None)

def change_pcard(pcard, **kwargs):
	vals = getattr(pcard).copy()
	vals.update(kwargs)
	return PositionedCard(**vals)

def is_in(card, cards):
	for c in cards:
		if card is c:
			return True
	return False

class Card():
	def __init__(self, colors, number):
		self.colors=colors
		self.number=number

	def __str__(self):
		return "%s  %s" % (self.colors, self.number)


class Hand():
	""" contains cards as unordered Counter() object of namedtuples"""

	def __init__(self, cards = []):
		self._cards = cards


	def cards_in(self, cards):
		self._cards += cards

	def cards_out(self, cards):
		self._cards -= cards

class Supplier():
	def __init__(self, size, location):
		self.size = size
		self.location = location

	def upgrade(self):
		self.size += 1

	def downgrade(self):
		self.size -= 1


class Supply():
	""" contains cards as namedtuples in an ordered list, cards coming in and out are assumed to be Counter()s of namedtuples """

	def __init__(self, cards):
		self._cards = cards

	def cards_out(self, out_cards):
		if out_cards > len(self.cards):
			return print('cannot supply that many cards')
		the_cards = self.cards[:out_cards]
		del self.cards[:out_cards]
		return the_cards

	def cards_in(self, cards):
		self._cards += cards
		



class Catalog():

	def __init__(self, positioned_cards):
		self._cards = positioned_cards

	def swap(self, old_card, new_card):
		pcard = find_pcard(old_card)
		change_pcard(pcard, card = new_card)
		change_pcard(pcard.south, north = new_card)
		change_pcard(pcard.north, south = new_card)
		change_pcard(pcard.west, east = new_card)
		change_pcard(pcard.east, west = new_card)

	def find_pcard(self, card):
		pcard = [pcard for pcard in self.pcards if pcard.card == card]
		if pcard == []:
			return print('this card is not in catalog')
		return pcard[0]

	def get_line(self, company):
		pcards = self.pcards
		home_card = company.supplier.location
		colors = home_card.colors
		def line_of_color(card, color, pcards, line = []):
			pcard = find_pcard(card)
			matching_neighbors = [card for card in [pcard.north, pcard.south, pcard.east, pcard.west] if card != None and color in card.colors and card not in line]
			if matching_neighbors == []:
				return line
			return [line_of_color(card, color, pcards, (line + matching_neighbors)) for card in matching_neighbors][0]
		return set(list(itertools.chain(*[line_of_color(card, color, pcards) for color in colors])))


class Company():
	"""
	attributes:
		name: str unique to Company instance
		hand: a list of Card objects
		supplier: an Supplier object with size and location
	"""

	def __init__(self, name, hand, supplier):
		self.name = name
		self._hand = hand
		self._supplier = supplier

	def take_turn(self, supply, catalog):
		#action = input('What would you like to do? supply, operate, or trade')
		#if action = 'operate':
		#	operate(self, TeaCards.supply, TeaCards.catalog)
		#if action = 'supply':
		#	supply(self, TeaCards.supply)
		#if action = 'trade':
		#	inputs = input('Please provide a location, a card to swap, and payment cards. (swap_location, swap_card, payment_cards)':)
		#		catalog.trade(self, catalog, supply, inputs)
		TeaCards.take_turn()

	def supply(self, supply):

		hand = self._hand
		size = self._supplier.size
		if len(hand) < size + 1:
			print('not enough cards to supply')
		supply.cards_in(hand)
		self._hand = []
		self._supplier.upgrade()

	def trade(self, catalog, supply, old_card, new_card, payment_cards):
		cost = max(old_card.number, new_card.numer)
		if cost > len(payment_cards):
			print('need more cards to trade')
		self.hand.cards_out(payment_cards)
		self.supply.cards_in(payment_cards)
		catalog.swap(old_card, new_card)

	def operate(self, supply, catalog):
		""" increases a company's hand size by either the company's line_size or supplier, whichever is smallest """
		def draw(self, number_of_cards):
			if number < 0 :
				return ('cannot draw negative amount')
			the_cards = supply.cards_out(number_of_cards)
			self._hand.cards_in(the_cards)

		supplier = self.supplier

		if sum(company.hand.values()) > supplier:
			return print('cannot operate, too many cards')

		line_size = len(catalog.get_line(self))
		difference = line - supplier

		if difference == 1 or difference == 0:
			draw(supplier)
		elif difference >= 2:
			company.supplier -= 1
			if supplier == 0:
				return print('You have under-operated out of business')
			draw((supplier - 2)),
		elif difference == -1:
			draw(line_size)
		elif difference <= -2:
			company.supplier -= 1
			if supplier == 0:
				print('You have over-operated out of business')
			draw(line)

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

	def eliminate_company(company):
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


