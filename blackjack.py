import random
import os
clear = lambda: os.system('clear')

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8, 'Nine': 9, 'Ten': 10, 'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11}

class Card:
	
	def __init__(self, rank, suit):
		self.rank = rank
		self.suit = suit
		self.value = values[rank]
	
	def __str__(self):
		return f'{self.rank} of {self.suit}'

class Deck:
	
	def __init__(self):
		self.deck = []  # start with an empty list
		for suit in suits:
			for rank in ranks:
				self.deck.append(Card(rank, suit))
	def __str__(self):
		for card in self.deck:
			print(card)
		return ''

	def shuffle(self):
		random.shuffle(self.deck)
		
	def deal(self):
		return self.deck.pop(0)

class Hand:
	def __init__(self):
		self.cards = []  # start with an empty list as we did in the Deck class
		self.value = 0   # start with zero value
		self.aces = 0	 # add an attribute to keep track of aces
	
	def add_card(self, new_card):
		total = 0
		self.cards.append(new_card)
		for card in self.cards:
			total += card.value
		self.value = total

	def adjust_for_ace(self):
		for card in self.cards:
			if card.rank == 'Ace' and self.value > 21:
				self.value -= 10

class Chips:
	
	def __init__(self):
		self.total = 100  # This can be set to a default value or supplied by a user input
		self.bet = 0
		
	def win_bet(self):
		self.total += self.bet * 2
	
	def lose_bet(self):
		self.total -= self.bet

def place_bet(total_chips):
	bet = 0
	while bet == 0:
		try:
			bet = int(input('Place a bet: '))
			print('')
			if (bet == 0):
				print('Invalid bet, please try again\n')
			elif (bet > total_chips):
				print(f'Invalid bet, your max bet is: {total_chips}\n')
				bet = 0
		except:
			print('Invalid bet, please try again\n')
			bet = 0
	return bet

def hit(deck, hand):
	hand.add_card(deck.deal())
	hand.adjust_for_ace()

def hit_or_stand(deck, hand):

	global playing  # to control an upcoming while loop
	
	move = ''
	while move not in ('H', 'S'):
		move = input('Hit or Stand? (h/s): ').upper()
		print('')
	if move == 'H':
		hit(deck, hand)
	else:
		playing = False

def show_some(player, dealer):

	print('Player Cards:')
	for card in player.cards:
		print(f'[ {card} ]')
	print(f'Total: {player.value}\n')

	print('Dealer Cards:')
	print(f'[ {dealer.cards[0]} ]')
	print(f'[ HIDDEN CARD ]')
	print(f'Total: {dealer.cards[0].value}\n')
	
def show_all(player, dealer):

	print('Dealer Cards:')
	for card in dealer.cards:
		print(f'[ {card} ]')
	print(f'Total: {dealer.value}\n')

def player_busts(chips):
	chips.lose_bet()
	global playing
	playing = False
	global player_lost
	player_lost = True
	print("Player BUST!\n")

def player_wins(chips):
	chips.win_bet()
	global playing
	playing = False
	print("Player wins!\n")

def dealer_busts(chips):
	chips.win_bet()
	print("Dealer BUST!\n")
	
def dealer_wins(chips):
	chips.lose_bet()
	print("Dealer wins!\n")
	
def push(): # Hands with the same sum called a "push"
	print('PUSH, round tied!\n')

'''
CODE EXECUTION STARTS HERE ********************************
'''
# Set up the Player's chips
playerChips = Chips()

while True:
	clear()
	# Print an opening statement
	print('GAME OF BLACKJACK\n')

	if playerChips.total == 0:
		print('Chips recharged to 100\n')
		playerChips.total = 100
	
	# Create & shuffle the deck, deal two cards to each player
	deck = Deck()
	deck.shuffle()
	playerHand = Hand()
	dealerHand = Hand()

	for i in range(0, 2):
		hit(deck, playerHand)
		hit(deck, dealerHand)
	
	# Prompt the Player for their bet
	playerChips.bet = place_bet(playerChips.total)
	
	# Show cards (but keep one dealer card hidden)
	show_some(playerHand, dealerHand)

	playing = True
	player_lost = False
	
	while playing:  # recall this variable from our hit_or_stand function
		
		if playerHand.value == 21:
			player_wins(playerChips)

		# Prompt for Player to Hit or Stand
		hit_or_stand(deck, playerHand)

		show_some(playerHand, dealerHand)

		if playerHand.value == 21:
			player_wins(playerChips)

		# If player's hand exceeds 21, run player_busts() and break out of loop
		if playerHand.value > 21:
			player_busts(playerChips)

	# If Player hasn't busted, play Dealer's hand until Dealer reaches 17
	show_all(playerHand, dealerHand)
	while dealerHand.value <= 17 and not player_lost:
		if dealerHand.value < playerHand.value:
			hit(deck, dealerHand)
		else:
			break
		show_all(playerHand, dealerHand)

	# Run different winning scenarios
	if dealerHand.value > 21:
		dealer_busts(playerChips)
	elif dealerHand.value == 21 or dealerHand.value > playerHand.value:
		dealer_wins(playerChips)
	elif dealerHand.value == playerHand.value:
		push()
	
	# Inform Player of their chips total
	print(f'Player Chips: {playerChips.total}\n')
	
	# Ask to play again
	play_again = ''
	while play_again not in ('Y', 'N'):
		play_again = input('Do you want to play again? (y/n): ').upper()
		print('')
	if play_again == 'N':
		break
