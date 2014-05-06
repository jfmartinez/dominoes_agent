#Authors: Jose F. Martinez Rivera, Adam Cancel
import random
import re
import copy


game_type = "Random"

#______________________________________________________________________________
# Minimax Search

def minimax_decision(state, game):
	"""Given a state in a game, calculate the best move by searching
	forward all the way to the terminal states. [Fig. 5.3]"""

	def agent_value(state):
		v = -100
		for a in game.ai_actions(state):
			v = max(v, p1_value(game.result(state, a)))
		return v

	def p1_value(state):
		v = 100
		for a in game.actions(state):
			v = min(v, p2_value(game.result(state, a)))
		return v

	def p2_value(state):
		v = -100
		for a in game.actions(state):
			v = max(v, p3_value(game.result(state, a)))
		return v

	def p3_value(state):
		v = 100
		for a in game.actions(state):
			v = min(v, agent_turn(game.result(state, a)))
		return v

	def agent_turn(state):
		return game.diversity(state)

	# Body of minimax_decision:
	return agent_value(state)


class DominoGame:
	def __init__(self):
		#dSomething
		self.dominoes = []

	def generateDominoes(self):
		#Generate domino tiles
		for f in range(0,7):
			for k in range(0,7):
				check = True #Check for previous tuples
				#Check if there's a previous domino made
				for tuple in self.tile_combinations:
					if sorted(tuple) == sorted((f,k)): #This makes (5,6) == (6,5)
						check = False
				#If check is true no previous domino was found		
				if check:
					self.tile_combinations.append((f,k))
		self.dominoes = []
		for tile_comb in self.tile_combinations:
			self.dominoes.append(Domino(str(tile_comb[0]), str(tile_comb[1])))

	def actions(self, state):
		actions = []
		left_side = state.get_edgeA()
		right_side = state.get_edgeB()

		for domino in self.dominoes:
			if domino in state.dominoes_played or domino in state.agent_hand:
				continue
			elif domino.hasSide(left_side) or domino.hasSide(right_side):
				actions.append(domino)
		return actions

	def ai_actions(self, state):
		actions = []
		left_side = state.get_edgeA()
		right_side = state.get_edgeB()

		for domino in state.agent_hand:
			
			if domino.hasSide(left_side) or domino.hasSide(right_side):
				actions.append(domino)
		return actions

	def result(self, state, action):

		state.dominoes_played.append(action)
		choice = random.randint(0,1)
		if choice == 0 and action.hasSide(state.get_edgeA):
			state.add_domino_action(action, "LEFT")
		elif choice == 1 and action.hasSide(state.get_edgeB):
			state.add_domino_action(action, "RIGHT")
		return state

	def diversity(self, state):
		dominos = [0,1,2,3,4,5,6]
		domino_tiles = [0,0,0,0,0,0]
		for domino in state.agent_hand:
			domino_tiles[domino.side_A_Value] = domino_tiles[domino.side_A_Value] + 1
			domino_tiles[domino.side_B_Value] = domino_tiles[domino.side_B_Value] + 1

		return domino_tiles



#Domino Class represents a domino object
class Domino:
	
	#Create domino tile
	def __init__(self, side_A, side_B):
		self.side_A = side_A #One side of the tile
		self.side_B = side_B #Other side of the tile

	#Print to the domino tile
	def __str__(self):
		return "("+self.side_A + "|" + self.side_B + ")"

	def __rpr__(self):
		return "("+self.side_A + "|" + self.side_B + ")"

	#Returns the value of the tile
	def get_value(self):
		return int(self.side_A) + int(self.side_B)

	#Returns true if the tile is double
	def is_double(self):
		return self.side_A == self.side_B

	#See if a tile matches with side A
	def match_sideA(self, tile):

		if self.side_A == tile.side_A:
			return "AA"
		elif self.side_A == tile.side_B:
			return "AB"
		else:
			return "N/A" #No Match

	#See if a tile matches with side B
	def match_sideB(self, tile):
		
		if self.side_B == tile.side_B:
			return "BB"
		elif self.side_B == tile.side_A:
			return "BA"
		else:
			return "N/A" #No Match
	#Flip the domino
	def flip(self):
		temp = self.side_A
		self.side_A = self.side_B
		self.side_B = temp

	def hasSide(self, side):
		if self.side_A == side:
			return True
		elif self.side_B == side:
			return True
		else:
			return False

	def hasBothSide(self, sideA, sideB):
		if self.side_A == sideA:
			if self.side_B == sideB:
				return True
		elif self.side_A == sideB:
			if self.side_B == sideA:
				return True
		else:
			return False		

	def side_B_Value():
		return int(self.side_B)
	def side_A_Value():
		return int(self.side_A)
#Game Board
class GameBoard:

	def __init__(self):
		self.name ="Daz Ruler"
		self.a_list = []
		self.b_list = []
		self.player_names = []
		self.player_tiles = [7,7,7,7]
		self.current_player = 0
		#self.player_points_on_board = [0,0,0,0]
		self.player_pass_values = []
		self.lead_player = 0
		self.winning_player = 0
		self.player_who_pass = ""
		self.domino_agent = 0
		self.finished = False
		self.dominoes_played = []


	def first_tile(self, tile):
		self.a_list.append(tile)
		self.b_list.append(tile)
		self.dominoes_played.append(tile)

	def add_agent(self, domino_hand):
		self.agent_hand = domino_hand

	#Append tile to one side of the board
	#It's important to know that all tiles will be connected strictly through side B to side A
	def place_tile(self,tile, side):

		#Choose to place the tile on one side
		if "LEFT" in side:
			edge_tile = self.a_list[-1]
			response = edge_tile.match_sideB(tile)
			print(response)
			if response == "BA":
				self.a_list.append(tile)
				#Move to next player
				self.update_player_number_tiles()
				self.next_player()
				self.dominoes_played.append(tile)


			elif response == "BB":
				tile.flip()
				self.a_list.append(tile)
				#Move to next player
				self.update_player_number_tiles()

				self.next_player()
				self.dominoes_played.append(tile)


		#Choose to place the tile on the other side
		elif "RIGHT" in side:
			edge_tile = self.b_list[-1]
			response = edge_tile.match_sideB(tile)
			if response == "BA":
				self.b_list.append(tile)
				#Move to next player
				self.update_player_number_tiles()
				
				self.next_player()
				self.dominoes_played.append(tile)

			elif response == "BB":
				tile.flip()
				self.b_list.append(tile)
				self.update_player_number_tiles()
		
				#Move to next player
				self.next_player()
				self.dominoes_played.append(tile)


		for i in range(0, 4):
			if self.player_tiles[i] == 0:
				self.finished = True
				print(self.player_names[i])


	#Prints out the left side of the board
	def get_sideA(self):
		listA = ""
		for tile in self.a_list:
			listA += str(tile)
		return listA

	#Returns a string representing the right side of the board
	def get_sideB(self):
		listB = ""
		for tile in self.b_list:
			listB += str(tile)
		return listB

	#Get the edge domino of the Left side
	def get_edgeA(self):
		return self.a_list[-1].side_B

	#Get the edge domino at the right side
	def get_edgeB(self):
		return self.b_list[-1].side_B

	#Players
	#Get current player name
	def	get_current_player(self):
		index =	self.current_player
		return self.player_names[index]


	#Add player
	def add_player(self,name):
		self.player_names.append(name)

	#Erase all players
	def erase_players(self,name):
		self.player_names = []	
	
	#Move Current Player Index to next index
	def next_player(self):

		if self.current_player == 3:
			self.current_player = 0
		else:
			self.current_player = self.current_player + 1

	#Set the player who will start
	def set_starting_player(self, name):
		index = self.player_names.index(name)
		self.current_player = index


	#Get how many tiles has a player
	def player_number_tiles(self,name):
		index = self.player_names.index(name)
		return self.player_tiles[index]

	#Update the number of tiles of a player (# -1)
	def update_player_number_tiles(self):
		self.player_tiles[self.current_player] = self.player_tiles[self.current_player] - 1

	#Save player points of tiles on board
	#def save_player_tiles_value(self,value):
	#	self.player_points_on_board[self.current_player] = self.player_points_on_board[self.current_player] + value

	#Calculate lead player by how many tiles he has left
	def calculate_lead_player(self):	
		self.lead_player = player_tiles.index(min(player_tiles))
		
	#Set the winning player of the overall tournament 
	def set_winning_player(self,value):	
		self.winning_player = value

	#Save the edge values when a player said pass.
	def set_player_pass(self):	
		self.next_player()			


	#Save the edge values when a player said pass.
	def get_player_pass(self):	
		return	self.player_who_pass		


	#Get domino agent turn
	def domino_agent_index(self):
		index = self.player_names.index("Carlitos")
		self.domino_agent = index

	def add_domino_action(self, tile, side):
	#Choose to place the tile on one side
		if "LEFT" in side:
			edge_tile = self.a_list[-1]
			response = edge_tile.match_sideB(tile)
			print(response)
			if response == "BA":
				self.a_list.append(tile)
				#Move to next player
				self.update_player_number_tiles()
				self.next_player()


			elif response == "BB":
				tile.flip()
				self.a_list.append(tile)
				#Move to next player
				self.update_player_number_tiles()

				self.next_player()

		#Choose to place the tile on the other side
		elif "RIGHT" in side:
			edge_tile = self.b_list[-1]
			response = edge_tile.match_sideB(tile)
			if response == "BA":
				self.b_list.append(tile)
				#Move to next player
				self.update_player_number_tiles()
				
				self.next_player()

			elif response == "BB":
				tile.flip()
				self.b_list.append(tile)
				self.update_player_number_tiles()
		
				#Move to next player
				self.next_player()

		#Game finished
		for i in range(0, 4):
			if self.player_tiles[i] == 0:
				self.finished = True
				print(self.player_names[i])

	
#Domino Player/Agent
class DominoAgent:

	def __init__(self, gameboard):
		self.name = "Carlitos"
		self.gameboard = gameboard
		self.game = DominoGame()


	#Receive Hand
	def establish_hand(self,hand):
		self.domino_hand = hand
		self.gameboard.add_agent(self.domino_hand)

	#Representation of a Hand
	def get_hand(self):
		hand_string = ""
		for i in self.domino_hand:
			hand_string += str(i) + ","
		return hand_string

	#For initial AI testing purposes, this makes the agent do a random move
	def ai_move(self):
		print(minimax_decision(copy.deepcopy(self.gameboard), self.game))
		
				
	#Viable tiles that can be played in an edge
	def getTilesWithSide(self, side):
		viable_tiles = []
		for i in self.domino_hand:
			if i.hasSide(side):
				viable_tiles.append(i)
		return viable_tiles

	def diversity(self, state):
		dominos = [0,1,2,3,4,5,6]
		domino_tiles = [0,0,0,0,0,0]
		for domino in self.dominoes_hand:
			domino_tiles[domino.side_A_Value] = domino_tiles[domino.side_A_Value] + 1
			domino_tiles[domino.side_B_Value] = domino_tiles[domino.side_B_Value] + 1

		return domino_tiles


	#Viable tiles that can be played in an edge that have both sides desired
	def getTilesWithBothSide(self, sideA, sideB):
		viable_tiles = []
		for i in self.domino_hand:
			if i.hasBothSide(sideA, sideB):
				viable_tiles.append(i)
		return viable_tiles	

	#Viable tiles that can be played in an edge but will make a player pass
	def getTilesWithSide(self, side):
		viable_tiles = []
		for i in self.domino_hand:
			if i.hasSide(side):
				viable_tiles.append(i)
		return viable_tiles	

	#The highest possible tile
	def getHighestValue(self, tiles):
		value = 0
		highest_tile = tiles[0]
		for i in tiles:
			if i.get_value() > value:
				highest_tile = i #Get the highest tile
				value = i.get_value()
		return highest_tile #Return the highest tile

	
#Domino Generator
class DominoGenerator:

	def __init__(self):
		self.tile_combinations = []
		self.dominoes = []
		self.generateDominoes()
		print(len(self.dominoes))
	
	def generateDominoes(self):
		#Generate domino tiles
		for f in range(0,7):
			for k in range(0,7):
				check = True #Check for previous tuples
				#Check if there's a previous domino made
				for tuple in self.tile_combinations:
					if sorted(tuple) == sorted((f,k)): #This makes (5,6) == (6,5)
						check = False
				#If check is true no previous domino was found		
				if check:
					self.tile_combinations.append((f,k))
		self.dominoes = []
		for tile_comb in self.tile_combinations:
			self.dominoes.append(Domino(str(tile_comb[0]), str(tile_comb[1])))
	
	def getRandomHand(self):
		player_hand = []
		for i in range(0,7):
			choice = random.randint(0, len(self.dominoes)-1)
			player_hand.append(self.dominoes.pop(choice))
		return player_hand

def print_hand(hand):
	hand_string = ""
	for i in hand:
		hand_string += str(i)
	print(hand_string)
	
#Domino Game Start
	
#Create Game Board instance
gameboard = GameBoard()

#Initialize Agent
our_player = DominoAgent(gameboard)

#Shuffle dominos
domino_shuffler = DominoGenerator()
for h in range(0, 3):
	player_name = input("Player #"+ str(h) + " name: ")
	gameboard.add_player(player_name)


gameboard.add_player(our_player.name)


#Randomized process for testing
if game_type == "Random":
	hands = []
	hands.append(domino_shuffler.getRandomHand())
	hands.append(domino_shuffler.getRandomHand())
	hands.append(domino_shuffler.getRandomHand())
	hands.append(domino_shuffler.getRandomHand())
	for k in hands:
		print_hand(k)
# our_player.establish_hand(hands[3])
agent_hand = []
for k in range(0,7):
	domino_text = input("Enter Domino #" + str(k) + ": ")
	if domino_text == "6|6":
		set_first_player = "Carlitos"
	else:
		agent_hand.append(Domino(domino_text[0], domino_text[2]))

for i in agent_hand:
	print(str(i))
#Establishes our agent's hand
our_player.establish_hand(agent_hand)
print(gameboard.player_names)

set_first_player = input("Who Play's First? ")

gameboard.set_starting_player(set_first_player)


first_domino = input("First Play: ")
if gameboard.get_current_player() == our_player.name:
	our_player.current_player

gameboard.first_tile(Domino(first_domino[0], first_domino[2]))
gameboard.next_player()
#Game loop
while not gameboard.finished:
	#Print who's turn is it
	print(gameboard.get_current_player() + "'s Turn")
	#Show game state
	print("LEFT: " + gameboard.get_sideA())
	print("RIGHT: " + gameboard.get_sideB())

	#Carlitos makes a move
	if gameboard.get_current_player() == our_player.name:
		print("Carlitos makes a move")
		our_player.ai_move()
	else:

		move = input("Input a move: ")
		#player can pass
		if move == "PASS":
			gameboard.set_player_pass()

		else:
			#Example of a move 3|2 LEFT
			verify = re.match("[0-6]\|[0-6] ((LEFT)|(RIGHT))", move)
			if verify:
				gameboard.place_tile(Domino(move[0], move[2]), move[4:])
			else:
				print("INVALID MOVE")
#Print who's turn is it
#Show game state
print("LEFT: " + gameboard.get_sideA())
print("RIGHT: " + gameboard.get_sideB())
