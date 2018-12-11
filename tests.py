import unittest
import structures
from structures import Card, PositionedCard, Hand, Supplier, Supply, Catalog, default_card, Company, flatten, TeaCards
from structures import RED, ORANGE, YELLOW, GREEN, BLUE, VIOLET
from collections import namedtuple
from copy import copy

cards = [Card({RED, GREEN}, 1), Card({RED, GREEN}, 2), Card({ORANGE, RED}, 3)]
pcards = [PositionedCard(cards[0], north = cards[1], east = cards[2]), PositionedCard(cards[1], south = cards[0]), PositionedCard(cards[2], west = cards[0])]

#	Tests for pure functions
class Test_Pure_Functions(unittest.TestCase):

	def test_change_pcard(self):
		pcard = pcards[0]
		card = cards[1]
		new_pcard = structures.change_pcard(pcard, card = card)
		self.assertEqual(pcard.north, new_pcard.north)
		self.assertEqual(pcard.south, new_pcard.south)
		self.assertEqual(pcard.east, new_pcard.east)
		self.assertEqual(pcard.west, new_pcard.west)
		self.assertEqual(new_pcard.card, card)
		new_pcard = structures.change_pcard(pcard, south = card)
		self.assertEqual(new_pcard.north, pcard.north)
		self.assertEqual(new_pcard.south, card)


	def test_is_in(self):
		card = Card({'red','green'}, 4)
		self.assertFalse(structures.is_in(card, cards))
		new_cards = cards + [card]
		self.assertTrue(structures.is_in(card, new_cards))

	def test_flatten(self):
		lists = [[1, 2, 3]]
		self.assertEqual(flatten(lists), [1, 2, 3])
		lists = [[1, 2, 3], [4]]
		self.assertEqual(flatten(lists), [1, 2, 3, 4])

		
#	Tests for Hand methods

class Test_Hands_cards_in(unittest.TestCase):

	def test_cards_in_by_one(self):
		hand = Hand()
		new_hand = hand.cards_in([cards[0]])
		self.assertEqual(new_hand._cards, [cards[0]])

class Test_Hands_cards_out(unittest.TestCase):

	def test_cards_out_by_one(self):
		hand = Hand(cards = [cards[0]])
		new_hand = hand.cards_out([cards[0]])
		self.assertEqual(new_hand._cards,[])

#	Tests Supplier methods

class Test_Supplier_upgrade(unittest.TestCase):

	def test_ugrade_by_one(self):
		supplier = Supplier(size = 1, location = cards[0])
		new_supplier = supplier.upgrade()
		self.assertEqual(new_supplier._size, 2)

class Test_Supplier_downgrade(unittest.TestCase):

	def test_downgrade_by_one(self):
		supplier = Supplier(size = 2, location = cards[0])
		new_supplier = supplier.downgrade()
		self.assertEqual(new_supplier._size, 1)

class Test_Supply_draw(unittest.TestCase):

	def test_draw(self):
		supply = Supply(cards = cards)
		cards_drawn = supply.draw(2)
		self.assertEqual(cards_drawn, cards[:2])


class Test_Supply_cards_in(unittest.TestCase):

	def test_cards_in_by_two(self):
		supply = Supply(cards = [cards[0]])
		new_supply = supply.cards_in([cards[1],cards[2]])
		self.assertEqual(new_supply._cards, [cards[0], cards[1],cards[2]])

class Test_Supply_cards_out(unittest.TestCase):

	def test_cards_out_by_two(self):
		supply =Supply(cards = [cards[0], cards[1],cards[2]])
		new_supply = supply.cards_out(2)
		self.assertEqual(new_supply._cards, [cards[2]])

#	Tests Catalog methods

class Test_Catalog_swap(unittest.TestCase):

	def test_swap(self):

		catalog = Catalog(positioned_cards = pcards)
		old_pcard = catalog.find_pcard(cards[0])
		
		new_card = Card(colors = {VIOLET, RED}, number = 1)
		new_catalog = catalog.swap(cards[0], new_card)
		self.assertEqual(len(catalog._cards), len(new_catalog._cards))
		new_pcard = new_catalog.find_pcard(new_card)
		self.assertEqual(new_pcard.north, old_pcard.north)
		self.assertEqual(new_pcard.south, old_pcard.south)
		self.assertEqual(new_pcard.east, old_pcard.east)
		self.assertEqual(new_pcard.west, old_pcard.west)

		north_neighbor = new_catalog.find_pcard(new_pcard.north)
		east_neighbor = new_catalog.find_pcard(new_pcard.east)

		self.assertEqual(north_neighbor.south, new_card)
		self.assertEqual(east_neighbor.west, new_card)



class Test_Catalog_find_pcard(unittest.TestCase):

	def test_find_card_basic(self):
		catalog = Catalog(positioned_cards = pcards)
		pcard = catalog.find_pcard(cards[0])
		self.assertEqual(pcard, pcards[0])

	def test_find_card_not_in_pcards(self):
		catalog = Catalog(positioned_cards = pcards)
		card = Card(colors = {}, number = 64)
		new_card = PositionedCard(card = card)
		self.assertEqual(catalog.find_pcard(card), new_card)

class Test_Catalog_get_neighbors(unittest.TestCase):

	def test_get_neighbors(self):
		catalog = Catalog(positioned_cards = pcards)
		self.assertEqual(catalog.get_neighbors(pcards[0]),[cards[1], default_card, cards[2], default_card])

class Test_Catalog_matching_neighbors(unittest.TestCase):

	def test_matching_neighbors(self):
		catalog = Catalog(positioned_cards = pcards)
		pcard = pcards[0]
		self.assertEqual(catalog.matching_neighbors(pcard, GREEN, []), [cards[1]])

class Test_Catalog_line_of_color(unittest.TestCase):

	def test_line_of_color(self):
		catalog = Catalog(positioned_cards = pcards)
		self.assertEqual(set(catalog.line_of_color(card = cards[0], color = GREEN, pcards = pcards)), set([cards[0], cards[1]]))

class Test_Catalog_get_line(unittest.TestCase):

	def test_get_line(self):
		catalog = Catalog(positioned_cards = pcards)
		company = Company(supplier = Supplier(location = cards[0]))
		self.assertEqual(catalog.get_line(company), {cards[0], cards[1], cards[2]})

#	Tests for Company methods
'''
class Test_Company_supply(unittest.TestCase):

	def test_supply_one_to_two(self):
		company = Company(supplier = Supplier(size = 1, location = cards[0]), hand = cards)
		supply = Supply(cards = [])
		company.supply(supply)
		self.assertEqual(company._supplier._size, 2)
		self.assertEqual(company._hand, [])
		self.assertEqual(supply._cards, cards)

class Test_Company_trade(unittest.TestCase):

	def test_trade_basic(self):
		company = Company(supplier = Supplier(size = 1, location = cards[0]), hand = Hand(cards = cards) )
		catalog = Catalog(positioned_cards = pcards)
		supply = Supply(cards = [])
		old_card = cards[0]
		new_card = Card(colors = {BLUE, VIOLET}, number = 2)
		payment_cards = company._hand._cards[:2]

		company._hand.cards_in([new_card])

		old_neighbors = catalog.get_neighbors(catalog.find_pcard(old_card))
		
		company.trade(catalog, supply, old_card, new_card, payment_cards)

		new_neighbors = catalog.get_neighbors(catalog.find_pcard(new_card))
		new_supply = payment_cards + [old_card]

		self.assertEqual(new_supply, supply._cards)
		self.assertEqual(company._hand._cards, [cards[2]])
		self.assertEqual(new_neighbors, old_neighbors)
'''
'''
class Test_Company_draw(unittest.TestCase):

	def test_draw(self):
		company = Company(supplier = Supplier(size = 1, location = cards[0]), hand = Hand(cards = []))
		supply = Supply(cards = copy(cards))
		company.draw(supply, 2)
		self.assertEqual(supply._cards, [cards[2]])
		self.assertEqual(set(company._hand._cards), set(cards[:2]))

class Test_Company_operate(unittest.TestCase):

	def test_operate_base(self):
		company = Company(supplier = Supplier(size = 2, location = cards[0]), hand = Hand(cards = []))
		supply = Supply(cards = copy(cards))
		catalog = Catalog(positioned_cards = copy(pcards))
		company.operate(supply, catalog)

		self.assertEqual(len(company._hand._cards), 2)
'''
#	Test methods on TeaCards

class Test_TeaCards_get_company(unittest.TestCase):

	def test_get_company(self):
		company = Company(supplier = Supplier(size = 1, location = cards[0]), hand = cards)
		tea_cards = TeaCards(catalog = [], supply = [], companies = [company])
		self.assertEqual(tea_cards.get_company(company), company)

class Test_TeaCards_replace_company(unittest.TestCase):

	def test_replace_company(self):
		company = Company(supplier = Supplier(size = 1, location = cards[0]), hand = cards)
		tea_cards = TeaCards(catalog = [], supply = [], companies = [company])
		new_company = Company(supplier = Supplier(size = 3, location = cards[0]), hand = cards)
		tea_cards.replace_company(company, new_company)
		self.assertEqual(tea_cards._companies[0], new_company)


class Test_TeaCards_supply(unittest.TestCase):

	def test_supply_one_to_two(self):
		company = Company(supplier = Supplier(size = 1, location = cards[0]), hand = cards, name = 'comp')
		supply = Supply(cards = [])
		tea_cards = TeaCards(catalog = [], supply = supply, companies = [company])

		new_company = Company(supplier = Supplier(size = 2, location = company._supplier._location))

		tea_cards.supply(company)
		self.assertEqual(tea_cards._companies[0]._supplier._size, 2)
		self.assertEqual(tea_cards._companies[0]._hand, [])
		self.assertEqual(tea_cards._supply._cards, cards)

class Test_TeaCards_trade(unittest.TestCase):

	def test_trade(self):

		catalog = Catalog(positioned_cards = pcards)
		supply = Supply(cards = [])
		old_card = cards[0]
		new_card = Card(colors = {BLUE, VIOLET}, number = 2)
		new_cards = flatten([cards, [new_card]])
		company = Company(supplier = Supplier(size = 1, location = cards[0]), hand = Hand(cards = new_cards) )
		payment_cards = company._hand._cards[:2]

		tea_cards = TeaCards(supply = supply, catalog = catalog, companies = [company])

		old_neighbors = tea_cards._catalog.get_neighbors(catalog.find_pcard(old_card))

		new_supply = payment_cards + [old_card]

		tea_cards.trade(company, catalog, supply, old_card, new_card, payment_cards)
		new_neighbors = tea_cards._catalog.get_neighbors(catalog.find_pcard(new_card))

		self.assertEqual(new_supply, tea_cards._supply._cards)
		self.assertEqual(tea_cards._companies[0]._hand._cards, [cards[2]])

class Test_TeaCards_operate(unittest.TestCase):
	
	def test_operate_basic(self):
		supply = Supply(cards = cards)
		catalog = Catalog(positioned_cards = pcards)
		company = Company(supplier = Supplier(size = 2, location = cards[0]), hand = Hand(cards = []))
		tea_cards = TeaCards(supply = supply, catalog = catalog, companies = [company])

		tea_cards.operate(company, supply, catalog)

		self.assertEqual(tea_cards._supply._cards, [cards[2]])
	
	def test_operate_over(self):
		supply = Supply(cards = cards)
		catalog = Catalog(positioned_cards = pcards)
		company = Company(supplier = Supplier(size = 5, location = cards[0]), hand = Hand(cards = []))
		tea_cards = TeaCards(supply = supply, catalog = catalog, companies = [company])

		tea_cards.operate(company, supply, catalog)
		print(supply.draw(3), 'DRAW')
		self.assertEqual(tea_cards._supply._cards, [])
		self.assertEqual(tea_cards._companies[0]._supplier._size, 4)
		self.assertEqual(tea_cards._companies[0]._hand._cards, cards)

	def test_operate_under(self):
		supply = Supply(cards = cards)
		additional_card = Card(colors = {BLUE, RED}, number = 1)
		additional_pcard = PositionedCard(card = additional_card, north = cards[0], south = cards[1], east = cards[2], west = cards[0])
		new_pcards = pcards + [additional_pcard]
		catalog = Catalog(positioned_cards = new_pcards)
		company = Company(supplier = Supplier(size = 2, location = additional_card), hand = Hand(cards = []))
		tea_cards = TeaCards(supply = supply, catalog = catalog, companies = [company])

		tea_cards.operate(company, supply, catalog)

		self.assertEqual(tea_cards._companies[0]._supplier._size, 0)






if __name__ == '__main__':
    unittest.main()