#Authors: Jose F. Martinez Rivera, Adam Cancel
import random
import re

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


#Game Board
class GameBoard:

	def __init__(self):
		self.name ="Daz Ruler"
		self.a_list = [Domino("6","6")]
		self.b_list = [Domino("6","6")]
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

		for i in range(0, 4):
			if self.player_tiles[i] == 0:
				self.finished = True



	def get_sideA(self):
		listA = ""
		for tile in self.a_list:
			listA += str(tile)
		return listA

	def get_sideB(self):
		listB = ""
		for tile in self.b_list:
			listB += str(tile)
		return listB

	def get_edgeA(self):
		return self.a_list[-1].side_B

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

		edgeA = self.get_edgeA
		edgeB = self.get_edgeB

		if edgeA not in self.player_pass_values:
			self.player_pass_values.append(self.get_edgeA())

		if edgeB not in self.player_pass_values:
			self.player_pass_values.append(self.get_edgeB())

		cp = self.get_current_player()
		da = self.domino_agent_index()

		if da == 1:
			if cp == 4:
				self.player_who_pass = "L"
			elif cp == (da+1):
				self.player_who_pass = "R"
			else:
				self.player_who_pass = "P"
		elif da == 4:
			if cp == 1:
				self.player_who_pass = "R"
			elif cp == (da-1):
				self.player_who_pass = "R"
			else:
				self.player_who_pass = "P"

		elif da == 2:
			if cp == 1:
				self.player_who_pass = "L"
			elif cp == 3:
				self.player_who_pass = "R"
			else:
				self.player_who_pass = "P"	

		elif da == 3:
			if cp == 4:
				self.player_who_pass = "R"
			elif cp == 2:
				self.player_who_pass = "L"
			else:
				self.player_who_pass = "P"	

		self.next_player()			


	#Save the edge values when a player said pass.
	def get_player_pass(self):	
		return	self.player_who_pass		


	#Get domino agent turn
	def domino_agent_index(self):
		index = self.player_names.index("Carlitos")
		self.domino_agent = index

	
#Domino Player/Agent
class DominoAgent:

	def __init__(self, gameboard):
		self.name = "Carlitos"
		self.gameboard = gameboard

	#Receive Hand
	def establish_hand(self,hand):
		self.domino_hand = hand

	#Representation of a Hand
	def get_hand(self):
		hand_string = ""
		for i in self.domino_hand:
			hand_string += str(i) + ","
		return hand_string

	#For initial AI testing purposes, this makes the agent do a random move
	def random_move(self):
		choice = random.randint(0,1)
		turn_pass = False
		if choice == 0: #Aim for the left side
			left_edge = self.gameboard.get_edgeA()
			viable_tiles = self.getTilesWithSide(left_edge)
			if len(viable_tiles) != 0:
				turn_pass = False
				highest_tile = self.getHighestValue(viable_tiles)
				self.gameboard.place_tile(self.getHighestValue(viable_tiles), "LEFT")
			else:
				print("PASS")
				turn_pass = True
 
		if choice == 0 and turn_pass: #Aim for the right side
			right_edge = self.gameboard.get_edgeB()
			viable_tiles = self.getTilesWithSide(right_edge)
			if len(viable_tiles) != 0:
				turn_pass = False
				highest_tile = self.getHighestValue(viable_tiles)

				self.gameboard.place_tile(self.getHighestValue(viable_tiles), "RIGHT")
			else:
				turn_pass = True

		if choice == 1:
			right_edge = self.gameboard.get_edgeB()
			viable_tiles = self.getTilesWithSide(right_edge)
			if len(viable_tiles) != 0:
				turn_pass = False
				highest_tile = self.getHighestValue(viable_tiles)

				self.gameboard.place_tile(self.getHighestValue(viable_tiles), "RIGHT")
			else:
				turn_pass = True

		if choice == 1 and turn_pass: #Aim for the right side
			left_edge = self.gameboard.get_edgeA()
			viable_tiles = self.getTilesWithSide(left_edge)
			if len(viable_tiles) != 0:
				turn_pass = False
				highest_tile = self.getHighestValue(viable_tiles)

				self.gameboard.place_tile(self.getHighestValue(viable_tiles), "LEFT")
			else:
				print("PASS")
				turn_pass = True
		if turn_pass:
			self.gameboard.set_player_pass()
		elif not turn_pass:
			self.domino_hand.pop(self.domino_hand.index(highest_tile))
				
	#Viable tiles that can be played in an edge
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
def game_start():
	
	#Create Game Board instance
	gameboard = GameBoard()

	#Initialize Agent
	our_player = DominoAgent(gameboard)

	#Shuffle dominos
	domino_shuffler = DominoGenerator()

	gameboard.add_player("Jose")
	gameboard.add_player("Raul")
	gameboard.add_player("Oscar")

	gameboard.add_player(our_player.name)
	

	#Randomized process for testing
	hands = []
	hands.append(domino_shuffler.getRandomHand())
	hands.append(domino_shuffler.getRandomHand())
	hands.append(domino_shuffler.getRandomHand())
	hands.append(domino_shuffler.getRandomHand())
	our_player.establish_hand(hands[3])

	for i in hands:
		print_hand(i)
	print(gameboard.player_names)
	
	set_first_player = input("Who Play's First? ")

	gameboard.set_starting_player(set_first_player)
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
			our_player.random_move()
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
