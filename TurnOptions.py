import numpy as np
from CompaniesAndReserviors import Company, get_line, build_catalog, build_deck

def draw(number, company):
	if number <= len(deck):
		company.hand.append(deck[:number])
		company.hand = company.hand[0]
		del deck[:number]
	else: 
		company.hand.append(deck[:len(deck[:len(deck)])])
		company.hand = company.hand[0]
		del deck[:len(deck)]
	return company.hand

def operate(company):
	"""
	parameter company: A class instance of player includes attributes: hand, supplier, and line.
	return: updated company treasury with cards from supply, and updated supply with cards removed.
	"""
	if len(company.hand) > company.supplier:
		return print('cannot operate, too many cards')
	line = len(company.line)
	supplier = int(company.supplier)
	difference = line - supplier
	if difference == 1 or difference == 0:
		draw(supplier, company)
	elif difference >= 2:
		company.supplier -= 1
		if supplier == 0:
			return print('You have under-operated out of business')
		draw((supplier - 1), company),
	elif difference == -1:
		draw(line, company)
	elif difference <= -2:
		company.supplier -= 1
		if supplier == 0:
			print('You have over-operated out of business')
		draw(line, company)
	return company.hand


def supply(company):
	"""
	parameter company: 
	return: company.hand w/ cards removed, and supply with cards added, and updated company.supplier.
	"""
	if len(company.hand) < comany.supplier + 1:
		return print('cannot supply, not enough cards')
	cost = len(company.hand)
	company.supplier += 1
	supplier = company.supplier
	deck.append(company.hand[:cost])
	del company.hand[:cost]

def switch(company, deck, catalog, card, card_list):
	"""
	parameter card: A card in company.hand to e switched in
	parameter card_list: A list of cards. The first in the list is the card to be replaced by card. The following elements are a chain of cards to switch.
	returns: updated catalog, hand, and supply.
	"""
	card_list.sort(key = lambda x: x.number)
	if card.number > card_list[0].number:
		cost = card.number
	else: 
		cost = card_list[0].number
	if cost > len(company.hand):
		return print('cannot make switch, not enough cards')
	card_list.reverse()
	deck.append(card_list[0])
	coord_list = []
	for index in range(len(card_list)):
		coords = np.where(catalog == card_list[index])
		coord_list.append(coords)
	print(coord_list)
	for index in range(len(card_list)):
		x = int(coord_list[index][0])
		y = int(coord_list[index][1])
		print('whole catalog', catalog)
		print(x, y)
		print('catalog[x][y]', catalog[x][y])
		if index == len(card_list) - 1:
			print('card', card)
			print('final', catalog)
			catalog[x][y] = card
			continue
		catalog[x][y] = card_list[index +1]
	del company.hand[company.hand.index(card)]
	del company.hand[:cost - 1]
	return catalog


deck = build_deck('Folklorus_deck.csv')
catalog = build_catalog(deck)

company = Company()
#print('before operation', company.hand)
company.line = get_line(company, catalog)
operate(company)
#print('after operation', company.hand)
#print('supplier', company.supplier)
#print('catalog before', catalog)
print(catalog[0][1])
if len(company.hand) >= company.hand[0].number:
	switch(company, deck, catalog, company.hand[0],[catalog[0][0], catalog[0][1]])
else:
	operate(company)
	switch(company, deck, catalog, company.hand[0],[catalog[0][0], catalog[0][1]])



#print('catalog after', catalog)