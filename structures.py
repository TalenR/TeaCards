from collections import namedtuple, Counter

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
	['card', 'north', 'south', 'east', 'west', 'company'])
PositionedCard.__new__.__defaults__ = (None, None, None, None, None, None)

def change_pcard(pcard, **kwargs):
	vals = getattr(pcard).copy()
	vals.update(kwargs)
	return PositionedCard(**vals)

class Hand():
	""" contains cards as unordered Counter() object of namedtuples"""

	def __init__(self, cards = Counter()):
		self._cards = cards


	def cards_in(self, cards):
		self._cards += cards

	def cards_out(self, cards):
		self._cards -= cards


class Supply():
	""" contains cards as namedtuples in an ordered list, cards coming in and out are assumed to be Counter()s of namedtuples """

	def __init__(self, cards):
		self._cards = cards

	def cards_out(self, out_cards):
		if out_cards > len(self.cards):
			return print('cannot supply that many cards')
		the_cards = self.cards[:out_cards]
		del self.cards[:out_cards]
		return Counter(the_cards)

	def cards_in(self, cards):
		self._cards += list(cards.elements())
		


"""
class Catalog(Object):

	def __init__(self, positioned_cards):
		self._cards = positioned_cards

	def swap(self, old_card, new_card):
		change_pcard(old_card, card = new_card)
		change_pcard(old_card.south, north = new_card)
		change_pcard(old_card.north, south = new_card)
		change_pcard(old_card.west, east = new_card)
		change_pcard(old_card.east, west = new_card)



	def get_line(self, company): 
		company_position = (card for card in self.pcards if card.company = company)
		cards_by_location = [self.pcards.index(company_position)]
		def matching_neihbors(pcard):
			for card in [pcard.north, pcard.south, pcard.east, pcard.west]:
				if self.pcards.index(card) in cards_by_location:
					continue
				cards_by_location += self.pcardscard
"""
# I decided to go back to representing the catalog as a nested list. The non-uniqueness of cards means our SNWE identifiers can demonstratably be non-unique. A 2D array seems to be the best way to garauntee a unique identifier for the cards. 
class Catalog():
	""" contains cards as namedtuples in 2D nested list """
	def __init__(self, cards):
		self.cards = cards

	def swap(self, card, location):
		""" replaces a card at location in catalog with card """
		x, y = (location[0], locatio[1])
		self.cards[x][y] = (card)

	def get_line_size(self, company):
		""" returns the number of cards connected by a direct line of similar colors to those of the company's location """
		comp_x, comp_y = company.location
		line = {(comp_x, comp_y)}
		company_colors = self.cards[comp_x][comp_y].colors
		x_bound, y_bound = (range(len(self.cards[0])), range(len(self.cards)))
		def get_line_card(line_colors, location):
			i, j = (location[0], location[1])
			neighbors = [(i+1,j),(i-1,j),(i,j+1),(i,j-1)]
			for neighbor in neighbors:
				x, y = neighbor[0], neighbor[1]
				if (x in x_bound) and (y in y_bound) and (x,y) not in line:
					common_colors = line_colors.intersection(self.cards[x][y].colors)
					if len(common_colors) > 0:
						line += (x,y)
						return get_line_card(common_colors, (x,y))
		get_line_card(company_colors, (comp_x, comp_y))
		return len(line)


class Company():
	"""
	attributes:
		name: str unique to Company instance
		hand: a Counter() oject of namedtuple cards
		supplier: an integer, "size" of company
		location: an (x,y) tuple describing company's location in the catalog
	"""

	def __init__(self, name, hand, supplier = 1, line_size, location):
		self.name = name
		self._hand = hand
		self._supplier = supplier
		self.line_size = line_size
		self.location = location

	def take_turn(self):
		action = input('What would you like to do? supply, operate, or trade':)
		if action = 'operate':
			operate(self, TeaCards.supply, TeaCards.catalog)
		if action = 'supply':
			supply(self, TeaCards.supply)
		if action = 'trade':
			inputs = input('Please provide a location, a card to swap, and payment cards. (swap_location, swap_card, payment_cards)':)
				trade(self, TeaCards.catalog, TeaCards.supply, inputs)
		TeaCards.take_turn()

	def supply(self, supply):
		""" increases the size of supplier and removes payment_cards from hand 
		Paramenters:
			payment_cards: Counter() object of namedtuple cards
		"""
		if sum(self.hand.values()) != self.supplier + 1
			print('please provide', self.supplier + 1, 'cards to supply')
		supply.cards_in(self._hand)
		self._hand = Counter()
		self.supplier += 1

	def trade(self, catalog, supply, swap_location, swap_card, payment_cards):
		""" swaps a card in the hand for one in the catalog, possibly continues to chain that card over others

		parameters: 
			swap_location: (x,y) tuple, the location of the card-to-be-swapped in the catalog
			swap_card: card in the hand which will end up at swap_location
			payment_cards: cards in the hand which are returned to the supply
		"""
		x, y = swap_location[0], swap_location[1]
		cost = max(swap_carp.number, catalog[x][y].number)
		if sum(payment_cards.values()) + 1 != cost:
			return print('please provide', cost, 'cards to swap this card')
		chain_end = (catalog[x][y])
		catalog.swap(swap_card, swap_location)
		supply.cards_in(payment_cards)
		self._hand.cards_out(swap_card)
		self._hand.cards_out(payment_cards)

		def chain(self, catalog, supply, swap_location, swap_card):
			""" allows trade function to be recursive without demanding more payment cards"""
			x, y = swap_location[0], swap_location[1]
			if catalog[x][y].number >= swap_card.number:
				return print('cannot chain a', swap_card.number,'on a ', catalog[x][y].number)
			chain_end = catalog.cards[x][y]
			catalog.swap(swap_card, swap_location)
			keep_chaining = input('keep chaining? y/n':)
			if keep_chaining = 'y':
				next_card = input('where would you like to chain next? (x,y)':)
				return chain(self, catalog, supply, next_card, chain_end)

		keep_chaining = input('keep chaining? y/n':)
			if keep_chaining = 'y':
				next_card = input('where would you like to chain next? (x,y)':)
				return chain(self, catalog, supply, next_card, chain_end)

		supply.cards_in(chain_end)


	def operate(self, supply, catalog):
		""" increases a company's hand size by either the company's line_size or supplier, whichever is smallest """
		def draw(self, number):
			if number < 0 :
				return ('cannot draw negative amount')
			the_cards = supply.cards_out(number)
			self._hand.cards_in(the_cards)

		supplier = self.supplier

		if sum(company.hand.values()) > supplier:
			return print('cannot operate, too many cards')

		line_size = catalog.get_line_size(self.name)
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
			card = namedtuple('card',['colors','number'])
			with open(deck_file,'r') as f:
				r = csv.reader(f, delimiter=',')
				cards = []
				rows = [card(*l) for l in r]
				for row in rows:
					color = set(row.colors.split(' '))
					num = int(row.number)
					cards.append(card(color,num))
			self.supply = cards

		get_deck(deck_file)

		def build_catalog(decK):
			pass

		build_catalog(self.supply)


