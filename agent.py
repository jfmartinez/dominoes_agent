#Authors: Jose F. Martinez Rivera, Adam Cancel
import random
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
		self.current_player = 1
		#self.player_points_on_board = [0,0,0,0]
		self.player_pass_values = []
		self.lead_player = 0
		self.winning_player = 0
		self.player_who_pass = ""
		self.domino_agent = 0



	#Append tile to one side of the board
	#It's important to know that all tiles will be connected strictly through side B to side A
	def place_tile(self,tile, side):
		#Choose to place the tile on one side
		if side == "LEFT":
			edge_tile = self.a_list[-1]
			response = edge_tile.match_sideB(tile)
			print(response)
			if response == "BA":
				self.a_list.append(tile)
				#Move to next player
				next_player()

			elif response == "BB":
				tile.flip()
				self.a_list.append(tile)
				#Move to next player
				next_player()

		#Choose to place the tile on the other side
		elif side == "RIGHT":
			edge_tile = self.b_list[-1]
			response = edge_tile.match_sideB(tile)
			if response == "BA":
				self.b_list.append(tile)
				#Move to next player
				next_player()

			elif response == "BB":
				tile.flip()
				self.b_list.append(tile)
				#Move to next player
				next_player()

	def get_sideA(self):
		listA = ""
		for tile in self.a_list:
			listA += tile.getTileString()

	def get_sideB(self):
		listB = ""
		for tile in self.b_list:
			listB += tile.getTileString()

	def get_edgeA(self):
		return a_list[-1].side_B

	def get_edgeB(self):
		return b_list[-1].side_B

	#Players
	#Get current player name
	def	get_current_player(self):
		index =	self.current_player
		return self.player_names.index(index)


	#Add player
	def add_player(self,name):
		self.player_names.append(name)

	#Erase all players
	def erase_players(self,name):
		self.player_names = []	
	
	#Move Current Player Index to next index
	def next_player(self):

		if self.current_player == 4:
			self.current_player = 1
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

		edgeA = get_edgeA
		edgeB = get_edgeB

		if edgeA not in player_pass_values:
		self.player_pass_values.append(get_edgeA())

		if edgeB not in player_pass_values:
		self.player_pass_values.append(get_edgeB())

		cp = get_current_player()
		da = domino_agent_index()

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


	#Save the edge values when a player said pass.
	def get_player_pass(self):	
		return	self.player_who_pass		


	#Get domino agent turn
	def domino_agent_index(self):
		index = self.player_names.index("Agent")
		self.domino_agent = index

	
#Domino Player/Agent
class DominoAgent:

	def __init__(self):
		self.name = "Fernando 2.0"

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
		if choice == 0: #Aim for the left side
			left_edge = gameboard.get_sideA()
			viable_tiles = getTilesWithSide(left_edge)
			if len(viable_tiles) != 0:
				gameboard.place_tile(getHighestValue(viable_tiles), "LEFT")
			else:
				print("PASS")

		else: #Aim for the right side
			right_edge = gameboard.get_sideA()
			viable_tiles = getTilesWithSide(right_edge)
			if len(viable_tiles) != 0:
				gameboard.place_tile(getHighestValue(viable_tiles), "RIGHT")
			else:
				print("PASS")
				
	#Viable tiles that can be played in an edge
	def getTilesWithSide(self, side):
		viable_tiles = []
		for i in self.domino_hand:
			if i.hasSide(side):
				viable_tiles.append(i)
		return viable_tiles

	#The highest possible tile
	def getHighestValue(self, tiles):
		highest_tile, value = 0
		for i in tiles:
			if(i.get_value > value):
				highest_tile = i #Get the highest tile
				value = i.get_value
		return highest_tile #Return the highest tile

#Domino Generator
class DominoGenerator:

	def __init__(self):
		self.tile_combinations = []
		self.dominoes = []		
	
	def generatorDominoes():
		#Generate domino tiles
		self.tile_combinations = []
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
			choice = random.randint(0, len(self.dominoes))
			player_hand.append(self.dominoes.pop(choice))
		return player_hand


